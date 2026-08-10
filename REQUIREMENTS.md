# Republic of City - Product Requirements & Technical Specification

## 1. Project Overview & Tech Stack
* **Frontend:** Flutter (Dart) with Glassmorphism UI, translucent panels, liquid gradients, and 3D ruby animations.
* **Backend:** Django & Django REST Framework (DRF) with PostgreSQL database.
* **Real-time & Sync Layer:** Firebase Real-time Database (for instant Likes/Support counts) & Firebase Cloud Messaging (FCM) for targeted notifications.
* **Background Tasks:** Celery + Redis (for time-based automated workflows like Achaar Sanhita and election phase shifts).

---

## 2. Core Architecture & User Flow Rules

### A. Authentication & Onboarding
* **Google Login Only:** Fast onboarding to prevent bot creation.
* **Device ID Binding:** Every vote and active session is bound to the physical device ID to prevent multi-account vote rigging.
* **Mohalla Allocation:** Users select their City and Mohalla from a dropdown during profile creation. 
* **Mohalla Lock & Requests:** Users cannot change their Mohalla manually once set. To change, they must submit a "Mohalla Change Request" which the Django Admin must approve. All requests freeze automatically when an election date is announced.

### B. Feed, Interactions & Concerns
* **Content Types:** Text, Photos, and Polls (Videos disabled to save storage).
* **Cross-Mohalla Access:** Users can view other Mohallas via dropdown. They can **Like, Dislike, Support, and Do Not Support**, but **Commenting is strictly blocked** to prevent inter-mohalla clashes. Likes from other mohallas show aggregate counts per mohalla, hiding individual user identities.
* **Concerns (Samasya):** Users can raise issues with images and details. Other users vote via **Support** or **Do Not Support**. High support increases the author's **Credibility Score**.
* **Global Pinned Posts:** Master/City Admin can pin announcements or local ads (e.g., Janta Dry Clean) to the top of any Mohalla feed with dynamic click/impression tracking.

### C. Election Simulation Engine
* **Strict Compliance Rule:** **NO Digital Voter Slips or fake IDs** will ever be generated (Google/Apple policy compliance). Voting happens exclusively via an internal secure digital poll system.
* **City Election (Supreme Minister - Every 3 Months):** 
  * *Day 1-5:* Nominations (Parcha) open. Requires minimum Credibility Score.
  * *Day 6:* Admin allocates seats and symbols to top 30 candidates.
  * *Day 6-10:* Campaigning (Prachar).
  * *Day 11:* Code of Conduct (Achaar Sanhita) applied automatically by Celery (Posting disabled).
  * *Day 12-13:* Secure Voting (1 Person = 1 Vote, routed via Redis queue to prevent traffic crashes).
  * *Day 14:* Results declared, feed unlocked.
  * *Day 15:* Oath-taking. Supreme Minister forms a Cabinet of **max 11 members**.
* **Mohalla Election (Mohalla Minister - Every 1 Month):**
  * *Day 1-2:* Nominations.
  * *Day 3:* Symbols allocation.
  * *Day 4-8:* Campaigning.
  * *Day 9:* Local Achaar Sanhita applied.
  * *Day 10:* Voting, counting, and results.
  * *Day 11:* Oath-taking. Mohalla Minister forms a Cabinet of **max 5 members**.

### D. VIP Visual Hierarchy & Badges
* **Supreme Minister:** Dark Maroon & Gold animated frame + 3D Red Ruby Badge + "Supreme Minister of [City]" title banner.
* **City Cabinet (11):** Violet Glassmorphism frame + Violet 3D Ruby Badge.
* **Mohalla Minister:** Dark Green & Silver frame + Green 3D Ruby Badge.
* **Mohalla Cabinet (5):** Grey Metallic frame + Grey 3D Ruby Badge.

### E. Leader Privileges (Executed via Flutter App + RBAC APIs)
* **Supreme Minister:** God-mode view across all Mohallas (Post, Comment, Like anywhere), issue direct Orders to any Mohalla, and flag/shadow-ban users for admin review.
* **City Cabinet Departments (11 Roles):** Home Minister (Mod queue & strikes), Public Works (Priority concerns), I&B Minister (FCM broadcasts), Law Minister (Appeals), Grievance, Cultural, Health, Education, Vigilance, Finance, and IT Ministers.
* **Mohalla Cabinet (5 Roles):** Deputy Minister, Infra Head, Moderation Head, PR Head, and Community Head.
* **Anonymous Whistleblower:** Option to report illegal activities anonymously (visible as anonymous post to public, tracked by Admin/SM).

### F. Moderation & 3-Strike Rule
* **Profanity Filter:** Regex-based bad-word block list managed via Admin panel.
* **Penalties:**
  * *1st Strike:* 6-hour Shadow Ban.
  * *2nd Strike:* 24-hour Ban.
  * *3rd Strike:* 3-day Ban.
  * *4th Strike:* Permanent Ban with public "Featured Banned Profile" badge in the Mohalla.

---

## 3. App Screens Structure (Total 35 Screens)
* **Onboarding & Auth (3):** Splash, Login, Profile Setup.
* **Core Main Feed (6):** Mohalla Home, Explore (Cross-Mohalla), Concerns Hub, Create Post/Concern, Notifications, My Profile.
* **Detailed Views (3):** Single Post Thread, Single Concern View, Other User Profile.
* **Election Ecosystem (5):** Election Commission Hub, Nomination Form, Candidate Manifesto, Secure Voting Booth, Live Results & Oath.
* **VIP Mantralaya (5):** Mantralaya Dashboard, Moderation Queue, Priority Action Room, Broadcast Center, Local Control.
* **Drawer & Legal (8):** City Samvidhan (Acts/Clauses), Leaderboard, Settings, Privacy Policy, App Disclaimer ("Virtual Simulation"), Developers Info, Engineered By (Dynamic Team list), Banned Notice.
* **Utilities & Modals (5):** Edit Profile, Search/Discover, Report Bottom-Sheet, Full-Screen Image Viewer, Offline/Error Screen.