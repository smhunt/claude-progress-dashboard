#!/usr/bin/env python3
"""
Claude Code Activity Script
Analyzes Claude Code session data to show usage statistics.
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


# Pricing per million tokens (Claude pricing as of late 2024)
PRICING = {
    "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00, "cache_read": 1.50, "cache_write": 18.75},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00, "cache_read": 0.08, "cache_write": 1.00},
    "default": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
}


def get_pricing(model: str) -> dict:
    """Get pricing for a model, with fallback to default."""
    return PRICING.get(model, PRICING["default"])


def parse_since(since_str: str) -> datetime:
    """Parse the --since argument into a datetime."""
    now = datetime.now()

    if since_str == "yesterday":
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif since_str == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif since_str == "week":
        return (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif since_str == "month":
        return (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Try to parse as ISO date
        try:
            return datetime.fromisoformat(since_str)
        except ValueError:
            # Try as number of days
            try:
                days = int(since_str)
                return (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
            except ValueError:
                raise ValueError(f"Cannot parse date: {since_str}")


def find_session_files(claude_dir: Path) -> list:
    """Find all JSONL session files in the Claude projects directory."""
    projects_dir = claude_dir / "projects"
    session_files = []

    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                for jsonl_file in project_dir.glob("*.jsonl"):
                    session_files.append((project_dir.name, jsonl_file))

    return session_files


def parse_session_file(filepath: Path, since: datetime) -> dict:
    """Parse a session file and extract relevant data."""
    sessions = defaultdict(lambda: {
        "messages": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "start_time": None,
        "end_time": None,
        "model": None,
        "git_branch": None,
    })

    try:
        with open(filepath, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                timestamp_str = entry.get("timestamp")
                if not timestamp_str:
                    continue

                # Parse timestamp
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    timestamp = timestamp.replace(tzinfo=None)  # Make naive for comparison
                except:
                    continue

                # Filter by date
                if timestamp < since:
                    continue

                session_id = entry.get("sessionId", "unknown")
                session = sessions[session_id]

                # Track time range
                if session["start_time"] is None or timestamp < session["start_time"]:
                    session["start_time"] = timestamp
                if session["end_time"] is None or timestamp > session["end_time"]:
                    session["end_time"] = timestamp

                # Track git branch
                if entry.get("gitBranch"):
                    session["git_branch"] = entry.get("gitBranch")

                # Extract usage data from assistant messages
                if entry.get("type") == "assistant" and "message" in entry:
                    msg = entry["message"]
                    session["messages"] += 1

                    if msg.get("model"):
                        session["model"] = msg["model"]

                    usage = msg.get("usage", {})
                    session["input_tokens"] += usage.get("input_tokens", 0)
                    session["output_tokens"] += usage.get("output_tokens", 0)
                    session["cache_read_tokens"] += usage.get("cache_read_input_tokens", 0)
                    session["cache_write_tokens"] += usage.get("cache_creation_input_tokens", 0)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return dict(sessions)


def calculate_cost(session: dict) -> float:
    """Calculate the cost for a session based on token usage."""
    model = session.get("model", "default")
    pricing = get_pricing(model)

    input_cost = (session["input_tokens"] / 1_000_000) * pricing["input"]
    output_cost = (session["output_tokens"] / 1_000_000) * pricing["output"]
    cache_read_cost = (session["cache_read_tokens"] / 1_000_000) * pricing["cache_read"]
    cache_write_cost = (session["cache_write_tokens"] / 1_000_000) * pricing["cache_write"]

    return input_cost + output_cost + cache_read_cost + cache_write_cost


def format_project_name(encoded_name: str) -> str:
    """Convert encoded project path to readable name."""
    # Format: -home-user-project-name -> project-name
    parts = encoded_name.split('-')
    # Skip leading empty and common path parts
    significant_parts = []
    skip_words = {'', 'home', 'user', 'Users', 'root'}
    for part in parts:
        if part not in skip_words:
            significant_parts.append(part)
    return '-'.join(significant_parts) if significant_parts else encoded_name


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude Code session activity")
    parser.add_argument("--since", default="today",
                       help="Show sessions since: yesterday, today, week, month, or ISO date")
    parser.add_argument("--claude-dir", default=os.path.expanduser("~/.claude"),
                       help="Path to Claude config directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    since = parse_since(args.since)
    claude_dir = Path(args.claude_dir)

    print(f"\n{'='*60}")
    print(f" Claude Code Activity Report")
    print(f" Since: {since.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    session_files = find_session_files(claude_dir)

    if not session_files:
        print("No session files found in", claude_dir / "projects")
        return

    all_sessions = {}
    project_stats = defaultdict(lambda: {
        "sessions": 0,
        "messages": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost": 0.0,
        "models": set(),
    })

    total_stats = {
        "sessions": 0,
        "messages": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost": 0.0,
    }

    for project_name, filepath in session_files:
        sessions = parse_session_file(filepath, since)

        for session_id, session in sessions.items():
            if session["messages"] == 0:
                continue

            cost = calculate_cost(session)
            session["cost"] = cost

            readable_project = format_project_name(project_name)
            all_sessions[session_id] = {
                "project": readable_project,
                **session
            }

            # Aggregate project stats
            ps = project_stats[readable_project]
            ps["sessions"] += 1
            ps["messages"] += session["messages"]
            ps["input_tokens"] += session["input_tokens"]
            ps["output_tokens"] += session["output_tokens"]
            ps["cache_read_tokens"] += session["cache_read_tokens"]
            ps["cache_write_tokens"] += session["cache_write_tokens"]
            ps["cost"] += cost
            if session["model"]:
                ps["models"].add(session["model"])

            # Aggregate total stats
            total_stats["sessions"] += 1
            total_stats["messages"] += session["messages"]
            total_stats["input_tokens"] += session["input_tokens"]
            total_stats["output_tokens"] += session["output_tokens"]
            total_stats["cache_read_tokens"] += session["cache_read_tokens"]
            total_stats["cache_write_tokens"] += session["cache_write_tokens"]
            total_stats["cost"] += cost

    if args.json:
        output = {
            "since": since.isoformat(),
            "total": total_stats,
            "by_project": {k: {**v, "models": list(v["models"])} for k, v in project_stats.items()},
            "sessions": all_sessions,
        }
        print(json.dumps(output, indent=2, default=str))
        return

    # Print summary by project
    if project_stats:
        print("Projects Active:")
        print("-" * 60)
        for project, stats in sorted(project_stats.items(), key=lambda x: -x[1]["cost"]):
            models = ", ".join(sorted(stats["models"])) if stats["models"] else "unknown"
            print(f"\n  {project}")
            print(f"    Sessions: {stats['sessions']}")
            print(f"    Messages: {stats['messages']}")
            print(f"    Input tokens: {stats['input_tokens']:,}")
            print(f"    Output tokens: {stats['output_tokens']:,}")
            print(f"    Cache read: {stats['cache_read_tokens']:,}")
            print(f"    Cache write: {stats['cache_write_tokens']:,}")
            print(f"    Models: {models}")
            print(f"    Cost: ${stats['cost']:.4f}")
    else:
        print("No sessions found since", since.strftime('%Y-%m-%d %H:%M'))
        return

    # Print totals
    print(f"\n{'='*60}")
    print("TOTALS")
    print("=" * 60)
    print(f"  Sessions: {total_stats['sessions']}")
    print(f"  Messages: {total_stats['messages']}")
    print(f"  Input tokens: {total_stats['input_tokens']:,}")
    print(f"  Output tokens: {total_stats['output_tokens']:,}")
    print(f"  Cache read tokens: {total_stats['cache_read_tokens']:,}")
    print(f"  Cache write tokens: {total_stats['cache_write_tokens']:,}")
    print(f"  Total cost: ${total_stats['cost']:.4f}")
    print()


if __name__ == "__main__":
    main()
