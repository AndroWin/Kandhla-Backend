# Antigravity AI Agent - Core Development Instructions

## 1. Output & Coding Standards (Strict)
* **Never provide code snippets:** Always write and generate full, complete, production-ready code files from top to bottom. No placeholders (`// write remaining code here`) are allowed.
* **Architecture Integrity:** Maintain strict separation between Flutter frontend, Django backend, and Firebase services as outlined in `REQUIREMENTS.md` and `SCHEMA.md`.
* **Security First:** Always enforce Role-Based Access Control (RBAC) in Django APIs and validate Device ID bindings to prevent vote rigging and unauthorized privilege escalation.

## 2. Mandatory Context & Reference Files (Strictly Enforced)
* **Core Blueprint Rules:** The AI agent must always maintain the complete project context strictly according to `REQUIREMENTS.md` and `SCHEMA.md`.
* **UI & Architecture Reference Files:** For any screen design, layout, flow, or system architecture, the agent MUST reference and use the following local HTML files:
  * `adminui.html`
  * `architecture.html`
  * `screensui.html`
  * `blueprint.html`
* **Stay Within Boundaries:** The agent must **never** drift outside or deviate from the features and rules defined in these reference files. 
* **Context Recovery Protocol:** If the agent ever forgets details, loses context, or starts a fresh session, it **must first read and ingest all of the above reference files** before generating any code or response.

## 3. Milestone Tracking & Execution Flow
* **Milestones Management:** The agent must maintain and continuously update a `milestones.md` file, recording every successfully completed task and milestone.
* **Mandatory Command Sequence:** Whenever the user issues a command or prompt, the agent must execute the following sequence **before processing further**:
  1. Read and review `milestones.md` to check current progress.
  2. Read and review all reference files (`REQUIREMENTS.md`, `SCHEMA.md`, `adminui.html`, `architecture.html`, `screensui.html`, `blueprint.html`) to load full context.
  3. Proceed with the requested task or further development process.

## 4. Communication & Tone
* **Tone:** Always communicate and document in natural, clear **Roman Hindi tone** during discussions, code comments (where appropriate), and summaries. Strictly avoid Urdu script or overly formal/robotic English when explaining logic.

## 5. Compliance & Safety Checks
* **App Store Policy:** Ensure zero implementation of any "Digital Voter Slip" or fake government ID generation. Voting must strictly rely on the internal secure digital poll system.
* **Error Handling:** Implement global exception handlers in both Flutter (dio/http error interceptors) and Django (middleware logging) to prevent unexpected app crashes.