# Republic of Kandhla - Development Milestones

---

## Phase 1: Backend Database Models & Django Setup

### ✅ Milestone 1.1 — Django Project Initialization
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `manage.py` — Django entry point created
  - `kandhla/` — Project config package created (settings, urls, wsgi, asgi, celery, utils)
  - `kandhla/settings.py` — Production-ready settings with PostgreSQL, DRF, JWT, Celery+Redis, Firebase, CORS, Logging
  - `kandhla/celery.py` — Celery app config for background tasks (election automation, vote processing)
  - `kandhla/utils.py` — Global DRF exception handler with structured JSON error responses

### ✅ Milestone 1.2 — Database Models (SCHEMA.md Complete Implementation)
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - **accounts app** — Custom User model (UUID PK, Google auth, Device ID binding, RBAC roles, Credibility Score, 3-Strike moderation)
  - **ecosystem app** — City, Mohalla, MohallaChangeRequest, Cabinet models
  - **content app** — Post (normal/announcement/ad/official_order + anonymous), Concern (Samasya with Support/Do Not Support voting)
  - **election app** — Election (7-phase cycle), Candidate (symbol allocation, manifesto), Vote (1-device-1-vote, hashed token security)

### ✅ Milestone 1.3 — Django Admin Configuration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - All 9 models registered with detailed admin classes
  - UserAdmin with RBAC, credibility, strike management
  - ElectionAdmin with candidate inline, phase control
  - VoteAdmin with strict read-only permissions (no add/edit/delete) for audit integrity
  - MohallaChangeRequest with list_editable for quick approve/reject

### ✅ Milestone 1.4 — URL Configuration & App Registration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Root URL conf with all 4 app includes
  - All apps registered in INSTALLED_APPS
  - `requirements.txt` with all Python dependencies

---

## Phase 2: Serializers, RBAC Permissions & REST API Views

### ✅ Milestone 2.1 — DRF Serializers (All Apps)
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - **accounts/serializers.py** — GoogleAuthSerializer, UserProfileSerializer (with city/mohalla names, computed properties), UserProfileSetupSerializer (Mohalla lock validation), UserMinimalSerializer
  - **ecosystem/serializers.py** — CitySerializer, CityDetailSerializer (with nested mohallas), MohallaSerializer, MohallaChangeRequestCreateSerializer (election freeze check, pending duplicate check), CabinetSerializer (VIP badge info), SamvidhanSerializer, EngineeredBySerializer
  - **content/serializers.py** — PostSerializer (anonymous whistleblower logic — Admin/SM can see real author), PostCreateSerializer (profanity filter, Achaar Sanhita check, minister permission for official_order/announcement), ConcernSerializer, ConcernCreateSerializer, InteractionSerializer (cross-mohalla validation)
  - **election/serializers.py** — ElectionSerializer (phase-aware vote count hiding), CandidateSerializer, NominationSerializer (Credibility >= 500, ban check, city/mohalla match), CastVoteSerializer (1-device-1-vote, device match, hashed token), ElectionResultSerializer

### ✅ Milestone 2.2 — RBAC Permission Classes
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `kandhla/permissions.py` — 8 permission classes:
    - IsNotBanned, IsCitizen, IsMinister, IsMohallaMinister, IsCityMinister
    - IsSupremeMinister (God-mode), IsAdminOrSupremeMinister, IsSameMohallaOrMinister

### ✅ Milestone 2.3 — Profanity Filter Module
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `kandhla/profanity.py` — Regex-based bad-word filter
  - check_profanity() — content validation ke liye
  - clean_text() — text sanitization utility
  - Database-loadable word list support (Admin panel se manage hogi)

### ✅ Milestone 2.4 — REST API Views (All Endpoints)
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - **accounts/views.py** — GoogleAuthView (token verify + JWT + dev mode), UserProfileView, UserProfileSetupView (population sync), OtherUserProfileView
  - **ecosystem/views.py** — CityListView, CityDetailView, MohallaListView, MohallaChangeRequestCreateView, MohallaChangeRequestListView, CabinetListView, SamvidhanView, EngineeredByView
  - **content/views.py** — MohallaFeedView (pinned posts at top), CreatePostView (profanity + Achaar Sanhita), CreateConcernView, ConcernListView, InteractionVoteView (Credibility Score boost)
  - **election/views.py** — ElectionListView, ElectionDetailView, CandidateListView, NominationView (Credibility check), CastVoteView (SHA-256 hashed token + Redis queue + F() atomic increment), ElectionResultsView (phase-gated)

### ✅ Milestone 2.5 — URL Routing (All Endpoints Active)
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - 5 auth endpoints, 8 ecosystem endpoints, 5 content endpoints, 6 election endpoints
  - Total: **24 API endpoints** fully wired

---

## Phase 3: Celery Tasks, Middleware, Signals & Automation

### ✅ Milestone 3.1 — Election Celery Tasks
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `election/tasks.py` — 5 tasks:
    - `advance_election_phase()` — Auto phase shift (Nomination → Allocation → ... → Completed) with Celery chaining
    - `activate_achaar_sanhita_task()` — Code of Conduct auto-enable (posting disabled)
    - `deactivate_achaar_sanhita_task()` — Code of Conduct auto-disable (feed unlocked)
    - `declare_election_results()` — Winner determination, role assignment, old cabinet deactivation
    - `process_vote_queue()` — Redis queue se vote payloads batch processing
    - `schedule_next_elections()` — Daily check for new election cycle (City: 90 days, Mohalla: 30 days)
  - Phase duration config: City (5d+1d+4d+1d+2d+1d) & Mohalla (2d+1d+4d+1d+1d+4h)

### ✅ Milestone 3.2 — Accounts Celery Tasks
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `accounts/tasks.py` — 4 tasks:
    - `check_ban_expiry()` — Auto ban lift (15 min interval, permanent bans excluded)
    - `apply_strike()` — 3-Strike system (6h → 24h → 72h → Permanent + Credibility penalty)
    - `boost_credibility()` — Credibility Score increment for support
    - `update_mohalla_populations()` — Daily population count sync

### ✅ Milestone 3.3 — Content Celery Tasks
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `content/tasks.py` — 4 tasks:
    - `auto_escalate_concerns()` — 50+ support = auto city_priority (30 min interval)
    - `moderate_flagged_content()` — Profanity scan + auto-strike on violation
    - `cleanup_old_posts()` — 6-month old normal posts cleanup (weekly)
    - `sync_interaction_counts()` — Firebase Realtime DB sync stub (5 min interval)

### ✅ Milestone 3.4 — Custom Middleware Stack
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `kandhla/middleware.py` — 4 middleware classes:
    - `RequestLoggingMiddleware` — API request logging with execution time
    - `BanCheckMiddleware` — Timed + permanent ban enforcement on every request
    - `AchaarSanhitaMiddleware` — Post creation blocking during Code of Conduct
    - `GlobalExceptionMiddleware` — Unhandled exception safety net (500 error catch)

### ✅ Milestone 3.5 — Django Signals
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `accounts/signals.py` — User creation logging, Mohalla population auto-sync on save/change
  - `election/signals.py` — Election announcement logging, Candidate approval logging
  - Apps' `ready()` methods updated to register signals

### ✅ Milestone 3.6 — Celery Beat Schedule Configuration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - 7 periodic tasks configured in `settings.py`:
    - Ban expiry (15 min), Vote queue (2 min), Concern escalation (30 min)
    - Population sync (daily), Election scheduling (daily), Post cleanup (weekly)
    - Firebase sync (5 min)
  - `kandhla/__init__.py` mein Celery app import for auto-discovery

---

## Phase 4: Firebase Integration & Setup

### ✅ Milestone 4.1 — Firebase Module Implementation
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - `kandhla/firebase.py` created
  - FCM Notifications implementation for Targeted Push Notifications
  - Realtime Database sync implementation for Posts interaction counts without overloading PostgreSQL
  - Updated `content/tasks.py` to trigger the sync function in Celery Beat

### ✅ Milestone 4.2 — Local Setup & Documentation
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Created `README.md` containing startup guidelines, prerequisites, server instructions, and Celery worker start commands.

---

## Phase 5: Flutter App (Frontend) Setup & Auth

### ✅ Milestone 5.1 — App Initialization & Auth Screens
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Created new Flutter project `kandhla_app`.
  - Added core dependencies: `provider`, `dio`, `shared_preferences`, `firebase_core`, `firebase_auth`.
  - Created base Glassmorphism Theme System (`AppTheme`, `GlassContainer`).
  - Created `SplashScreen` with 3D Ruby simulation and authentication check.
  - Created `LoginScreen` with Google login button and Mohalla lock dropdown.
  - Created `ProfileSetupScreen` to capture name, bio, and submit to Django API.
  - Wired routing in `main.dart`.

### ✅ Milestone 5.2 — Core Feed
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Configured `ApiService` using Dio for network calls and interceptors.
  - Setup `UserProvider` to manage global profile, role, and credibility state.
  - Created `MainLayout` bottom navigation wrapper (Feed, Explore, Post, Profile).
  - Developed UI for `HomeFeedScreen` (Mohalla feed), `ExploreScreen`, `CreatePostScreen` and `ConcernsScreen` (Samasya hub).
  - Wired navigation from Auth flow to `MainLayout`.

### ✅ Milestone 5.3 — Django API Integration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Created `PostModel` and `UserProfileModel` to parse DRF responses.
  - Modified `ApiService` to point to Android emulator's localhost (`10.0.2.2:8000/api/`).
  - Integrated `LoginScreen` to hit `/api/auth/google/` with mock dev token and save JWT.
  - Integrated `ProfileSetupScreen` to hit `/api/auth/profile/setup/` using PUT method.
  - Built `FeedService` to fetch paginated content from `/api/feed/<mohalla_id>/`.
  - Upgraded `HomeFeedScreen` to use a `FutureBuilder` rendering live posts.
  - Wired `CreatePostScreen` to submit posts via `/api/posts/create/`.

### ✅ Milestone 5.4 — Interactions & Samasya Hub API Integration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Created `ConcernModel` to parse DRF responses for concerns.
  - Added interaction (`submitInteraction`) and concern fetching (`fetchConcerns`, `createConcern`) logic to `FeedService`.
  - Upgraded `HomeFeedScreen` to allow clicking upvote/downvote and executing optimistic local state updates.
  - Upgraded `ConcernsScreen` to use a `FutureBuilder` rendering live concerns from API.
  - Wired Support and Reject logic in `ConcernsScreen` for interactive voting.
  - Updated `CreatePostScreen` to conditionally call `FeedService.createConcern` when the 'Concern' tab is selected.

### ✅ Milestone 5.5 — Explore & Elections API Integration
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Created `EcosystemModel` and `ElectionModel` for data parsing.
  - Built `EcosystemService` to fetch cities and mohallas, and `ElectionService` for voting mechanisms.
  - Integrated `ExploreScreen` with live API data using expansion tiles for Mohallas.
  - Updated `ProfileScreen` with an "Election Hub" navigation button.
  - Developed `ElectionScreen` (and `VotingScreen`) for interacting with live elections and casting secure votes via the API.

### ✅ Milestone 5.6 — UI Refinements & Edge Cases
- **Date:** 2026-08-07
- **Status:** COMPLETED
- **Details:**
  - Resolved 17 `flutter analyze` linter warnings (super parameters, unused imports, deprecated `.withOpacity` and `.background`).
  - Implemented a dynamic `ProfileScreen` powered by `UserService` to fetch live user data.
  - Handled 401 Unauthorized globally in `ApiService` with automatic logout via a global `NavigatorKey`.
  - Upgraded empty states in Feed, Concerns, Explore, and Elections screens for a more polished and visually appealing experience.

---

## Phase 6: Ecosystem Refinements & Samvidhan
- **Status:** COMPLETED
- **Details:**
  - Implemented VIP Profiles UI with `rubyGreen`, `rubyGrey` gradients.
  - Developed `CustomDrawer` with global navigation links.
  - Built `SamvidhanScreen` displaying the constitution.
  - Created `LeaderboardScreen` showcasing the top 5 citizens based on credibility.
  - Linked all drawer elements.
  - Added Official Order and Whistleblower API payload structures.

---

## Phase 7: Edge Cases, Testing, and UI Polish
- **Status:** **COMPLETED**
- **Changes:**
  - Added `OfflineErrorScreen` to handle network disconnects via Dio interceptors.
  - Added `BannedNoticeScreen` for permanently suspended accounts (403 errors).
  - Built `ImageViewerScreen` with Hero animations for interactive full-screen image viewing in Concerns.
  - Implemented implicit animations (`AnimatedSwitcher`) for upvote and downvote counts in `HomeFeedScreen` and `ConcernsScreen`.
  - Added local searching capability (Search bar) inside `ExploreScreen` to filter cities seamlessly.
  - Resolved 10 `flutter analyze` lints and syntax errors.

---

## Phase 8: Finalizing the UI Ecosystem
- **Status:** **COMPLETED**
- **Changes:**
  - Implemented `NotificationsScreen` with dynamic type icons (system, interaction, alert).
  - Implemented `SinglePostScreen` with inline comment interactions.
  - Implemented `OtherProfileScreen` displaying specific role styling and credibility.
  - Created `MantralayaDashboard` hub for VIP Ministers (Mod Queue, Priority Room, Broadcast, Local Control).
  - Created `NominationScreen` (Parcha Bharo) handling eligibility logic based on credibility score.
  - Built static drawer utility screens (`Settings`, `Privacy`, `Disclaimer`, `Dev Info`, `Engineered By`).
  - Added `ReportModal` bottom sheet utility for reporting content/citizens.
  - 100% compliance with `screensui.html` and `flutter analyze` zero issues.

---

## Phase 9: Finalizing 100% Requirements Completion (35/35 Screens)
- **Status:** **COMPLETED**
- **Changes:**
  - Audited the `REQUIREMENTS.md` file and verified the "Total 35 Screens" requirement.
  - Built `SingleConcernScreen` for detailed view and voting on samasya (concerns).
  - Built `LiveResultsScreen` containing real-time animated bars for election tracking and Oath initialization.
  - Built `EditProfileScreen` for modifying citizen details.
  - The Flutter ecosystem is officially fully realized to exactly 35 distinct UI modules.

---

## Phase 10: End-to-End API Integration
- **Status:** **COMPLETED**
- **Changes:**
  - Verified and successfully migrated the database to ensure all 9 Django models (`accounts`, `ecosystem`, `content`, `election`) are active.
  - Executed a seed script (`seed_db.py`) to auto-populate the platform with testing data: Cities (Kandhla), Mohallas, a Superuser (Supreme Minister), initial normal posts, and priority concerns.
  - Removed dummy testing UUIDs from the Flutter service layer (`feed_service.dart`, `home_feed_screen.dart`, `concerns_screen.dart`).
  - Synced Flutter's frontend `mohallaId` parameters to fetch live dynamically seeded data from the local Django database.
  - 100% compliance with `flutter analyze` ensuring zero issues and a clean repository for deployment.

---

## Phase 11: Firebase Integration & Auth Finalization
- **Status:** **COMPLETED**
- **Changes:**
  - Connected the Flutter frontend to the active Firebase project `diz-chunaav-app` utilizing `flutterfire configure`.
  - Added `google_sign_in` and `firebase_messaging` dependencies.
  - Implemented the actual Firebase Google Sign-In pipeline in `LoginScreen` (`_handleGoogleLogin`) to retrieve the `idToken`.
  - Successfully fetched the FCM device token via `FirebaseMessaging.instance.getToken()` to map physical devices to voting profiles.
  - Updated `main.dart` with `Firebase.initializeApp()` and registered a top-level `@pragma('vm:entry-point')` handler for background push notifications.
  - Passed the `flutter analyze` linter checks completely with zero issues.

---

## Phase 12: Real-time DB Sync & Native App Configuration
- **Status:** **COMPLETED**
- **Changes:**
  - AI-generated a premium "Republic of Kandhla" logo for App Icon and Splash Screen assets.
  - Successfully integrated `flutter_launcher_icons` and `flutter_native_splash` via `pubspec.yaml` to generate native Android and iOS configurations.
  - Upgraded `HomeFeedScreen` interactions to stream real-time Likes/Dislikes instantly using a `StreamBuilder` listening directly to Firebase Realtime Database (`/interactions/posts/{id}`).
  - Maintained 100% clean codebase with zero `flutter analyze` issues.

---

## Phase 13: Free Backend Deployment Configuration
- **Status:** **COMPLETED**
- **Changes:**
  - Modified `requirements.txt` to include `dj-database-url` and `whitenoise` for cloud deployment.
  - Rewrote `settings.py` `DATABASES` logic to dynamically parse Supabase PostgreSQL connection strings via environment variables.
  - Added `WhiteNoiseMiddleware` to efficiently serve Django static files on Render without needing Nginx.
  - Authored a clean `build.sh` script to automate Render's CI/CD pipeline (install, collectstatic, migrate).
  - Verified codebase integrity locally with `python manage.py check` passing completely.

---

## Phase 14: Apple Sign-In (App Store Compliance)
- **Status:** **COMPLETED**
- **Changes:**
  - Added `apple_id` to the `User` model in Django and successfully applied migrations.
  - Implemented `AppleAuthView` in `accounts/views.py` using `PyJWT` to verify the Apple Identity Token and securely handle user login/registration.
  - Added the `sign_in_with_apple` package to Flutter's `pubspec.yaml`.
  - Upgraded `login_screen.dart` with a native `SignInWithAppleButton` that conditionally appears only on iOS devices (`TargetPlatform.iOS`).
  - Added `com.apple.developer.applesignin` entitlement to macOS and iOS native Xcode projects.
  - Validated integration with 0 issues in `flutter analyze` and `python manage.py check`.
