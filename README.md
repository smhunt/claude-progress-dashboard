# Claude Multi-Project Stand-Up Dashboard

Auto-updated every 30 minutes.

---

## wine-story-app

# Stand-Up Report

**Date:** 2025-12-09
**Project:** wine-story-app

---

## What was done since last update
- Updated README.md with latest features and info
- Replaced emojis with Ionicons for consistent mono/two-tone styling
- Fixed iOS 18 status bar with SafeAreaProvider wrapper
- Expanded wine database to 5,000 wines with LCBO URLs
- Added in-app changelog modal (v1.7.0)
- Curated 50+ Canadian wines from verified Ontario producers

## What code/files changed
- `app/_layout.tsx` - SafeAreaProvider + status bar fix
- `app/index.tsx` - Emoji → Ionicons, changelog modal
- `app/story.tsx`, `app/history.tsx` - Icon replacements
- `src/components/CanadianAlternatives.tsx` - All emojis replaced
- `src/data/lcbo-wines.json` - 5000 wines with LCBO URLs
- `src/data/top-100-lcbo-wines.json` - Bestsellers with real product IDs

## Blockers or dependencies
- None currently

## Next actions for Claude
- Await further feature requests
- Monitor for iOS 18 compatibility issues

## Next actions for human
- Test wine identification with real bottles
- Consider deploying to TestFlight for broader testing

---

## computer-vision-utility-monitor

# Stand-Up Report

**Date:** 2025-12-09
**Project:** computer-vision-utility-monitor

---

## What was done since last update
- Security hardening: removed hardcoded credentials from docker-compose.yml
- All passwords now use environment variables (Postgres, Grafana, InfluxDB)
- Added Catalyst UI components for dashboard (form controls, layout, data display)
- Updated .env.example with comprehensive template
- Merged feature/react-full-ui into main (complete React UI rebuild)

## What code/files changed
- `docker-compose.yml` - Environment variable references for all secrets
- `src/database/connection.py` - Removed hardcoded password defaults
- `dashboard/` - Catalyst UI components (sidebar, navbar, table, forms)
- `.env.example` - Full credential template
- `.gitignore` - Ignore meter snapshot logs and PDFs

## Blockers or dependencies
- Wyze Cam V2 firmware configuration pending
- Camera positioning and lighting optimization needed

## Next actions for Claude
- Assist with camera calibration when hardware is ready
- Implement additional meter types if requested

## Next actions for human
- Set up .env.local with actual credentials
- Position camera on water meter
- Test meter reading accuracy in various lighting conditions

---

## cursor-test

# Stand-Up Report

**Date:** 2025-12-09
**Project:** cursor-test

---

## What was done since last update
- Security fix: removed hardcoded SQL password
- Added environment variable placeholders for credentials
- Created .env.example with configuration template
- Updated .gitignore to exclude sensitive files and build artifacts
- Updated TlcContext to read connection string from environment

## What code/files changed
- `TLC-API/` - Connection string now from environment
- `.env.example` - New template file
- `.gitignore` - Exclude .env, bin/, obj/, etc.

## Blockers or dependencies
- None currently

## Next actions for Claude
- Await further development requests
- Assist with .NET 8 migration if needed

## Next actions for human
- Create .env file with actual SQL credentials
- Consider migrating to newer .NET patterns

---

## DotNet8

# Stand-Up Report

**Date:** 2025-12-09
**Project:** DotNet8

---

## What was done since last update
- Security fix: removed hardcoded SA_PASSWORD from docker-compose.yml
- Password now uses ${SA_PASSWORD} environment variable reference
- Created .env.example template for required environment variables

## What code/files changed
- `docker-compose.yml` - SA_PASSWORD now from env var
- `.env.example` - New template file

## Blockers or dependencies
- None currently

## Next actions for Claude
- Await further development requests
- Assist with CartWebApp features if needed

## Next actions for human
- Create .env file with actual SA_PASSWORD
- Test Docker Compose with SQL Server container

---

## app-booker-ontario-med-clinics

# Stand-Up Report

**Date:** 2025-12-09
**Project:** app-booker-ontario-med-clinics

---

## What was done since last update
- Made sign-in collapsible on booking form (compact button, expands on click)
- Added dynamic LAN links between clinic variants on About page
- Improved mobile layout: sticky step indicator, vertical field stacking
- Added hamburger menu for mobile navigation
- Fixed viewport height on iOS (100dvh) and added notch support
- Merged monorepo refactor with veterinary clinic and chat AI

## What code/files changed
- `apps/vet-clinic/` - Booking form mobile improvements
- Layout components - Hamburger menu, sticky header
- About page - Dynamic hostname for LAN links
- `index.html` - viewport-fit=cover, apple-mobile-web-app meta tags

## Blockers or dependencies
- None currently

## Next actions for Claude
- Await further feature requests
- Assist with additional clinic variants if needed

## Next actions for human
- Test booking flow on mobile devices
- Consider deploying vet clinic variant

---

## kindred-app

_no stand-up found_

---

## quadrant-vector-search-platform

_no stand-up found_

---

## gh-repo-creator

_no stand-up found_

---

## meter-reader-app-bygoogleaistudio

_no stand-up found_

---

## Claude-News-chrome-extension

# Stand-Up Report

**Date:** 2025-12-09
**Project:** Claude-News-chrome-extension
**Branch:** main

---

## Recent Work
- Merged PR #2 with Copilot updates
- Fixed version format, removed tts permission, fixed theme toggle
- Implemented Claude Code Digest Chrome extension
- Added YouTube players integration
- Initial plan and commit

## Current Status
- Chrome extension for Claude Code news/digest
- YouTube player integration working
- Theme toggle functional

## Blockers
- None

## Next Actions
- Publish to Chrome Web Store
- Add more news sources
- Improve UI/UX

---

