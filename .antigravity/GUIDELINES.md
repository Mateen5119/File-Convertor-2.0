# Software Development & Architecture Standards (2026)

## 1. Project Initiation & Architecture
* **Requirements & Scope:** Define PRD / SRS, user stories, acceptance criteria, and non-functional requirements (latency, availability, cost). Document Definition of Done, out-of-scope items, and a risk register (top 10 risks + owners).
* **UX/UI Design:** Map user flows, wireframes, and clickable prototypes. Define design system basics (colors/typography/components) and responsive breakpoints. Ensure WCAG 2.2 accessibility (keyboard navigation, contrast, focus states, error messages).
* **Architecture Strategy:** Default to modular monoliths or microservices. Prioritize an API-First design using OpenAPI/Swagger 3.1 as the source-of-truth. Document contracts, auth, and error formats before coding.
* **Technical Design:** Maintain high-level architecture diagrams (use Mermaid or Excalidraw) detailing clients, APIs, DBs, queues, and third parties. Define ERD, API boundaries, caching strategy, and basic threat modeling (assets, entry points, abuse cases).
* **Architecture Decision Records (ADRs):** Document technical choices in Markdown explaining the *why* and trade-offs.
* **Infrastructure as Code (IaC):** Provision resources programmatically via Terraform or OpenTofu instead of manual setup.

## 2. API & Integration Contracts
* **Lifecycle:** Enforce semantic versioning (SemVer) and document deprecation policies.
* **Testing:** Deploy mock servers and run contract tests for critical endpoints.
* **Autonomy:** Ensure frontend, mobile, and backend teams can operate independently against the OpenAPI spec.

## 3. Source Control, Collaboration & Environments
* **Version Control:** Standardize on Git + GitHub/GitLab using GitHub Flow (trunk-based or short-lived feature branches).
* **Branch Strategy:** Require mandatory PR reviews, branch protection, specific quality checks, and CODEOWNERS. `main` must remain deployable. Use Conventional Commits (`feat:`, `fix:`, `chore:`) and automated changelogs.
* **Coding Standards:** Enforce consistency with linters, formatters, and pre-commit hooks. Document project structure, naming conventions, and dependency rules. Use strict types.
* **Environment Isolation:** Maintain isolated configurations (`.env.local`, `.env.staging`, `.env.production`). Never risk user data during testing; ensure a separate database per environment.

## 4. Dependency & Package Management
* **Philosophy:** Minimize dependencies to reduce the attack surface. Prioritize pure-language implementations and raw runtime stream parsers (e.g., `pypdf`, `pdfplumber`) over bloated OS-level binaries or unverified third-party wrappers.
* **Version Control:** Pin exact versions in `package-lock.json` or `requirements.txt`.
* **Auditing:** Conduct regular audits (`npm audit`, `pip-audit`). Establish SLA requirements for dependency patching (e.g., critical within 48–72h).
* **Automation:** Utilize Dependabot or Renovate for automated update PRs.

## 5. Cybersecurity (DevSecOps) & Supply Chain
* **Authentication:** Default to Passkeys (FIDO2), OAuth 2.1/OIDC, or short-expiry JWTs + refresh tokens. Enforce MFA for staff, strong password policies, robust session management, and strict rate limiting (e.g., `express-rate-limit`).
* **Authorization:** Implement RBAC/ABAC. Enforce server-side checks for all sensitive actions. Assume Zero-Trust for internal microservice communications.
* **Secrets Management:** **NEVER** hardcode credentials, API keys, signing secrets, or fallback mock strings. Inject variables via centralized vaults (HashiCorp Vault) in production. Locally, manage via `.env` and mandate schema validation at runtime (e.g., `Zod`, `Joi`, `pydantic-settings`). Add `.env` and `*.pem` to global `.gitignore`.
* **Data Security:** Ensure HTTPS/TLS 1.3 everywhere. Hash passwords using bcrypt or Argon2. Prevent CSRF, enforce secure headers, and validate input/encode output to prevent XSS and SQL injections.
* **Secure File Processing:**
  * Validate file headers (magic bytes) to guarantee formats (PDF, WORD, JSON, HTML, Markdown) before memory ingestion.
  * Prevent DoS by enforcing max execution timeouts and file size limits (e.g., max 10MB).
  * Process transformations in isolated temporary directories. Scrub files immediately via `finally` blocks.
* **Frameworks & Compliance:** Align with NIST SSDF, OWASP Top 10, OWASP ASVS (Target L1/L2), OWASP SAMM, and ISO/IEC 27001 ISMS concepts.
* **Supply-chain Security:** Generate SBOMs (CycloneDX/SPDX) per release. Enforce SLSA provenance (tamper resistance). Require signed releases/artifacts, protected CI runners, and minimal permissions.

## 6. Database Management
* **Architecture:** Utilize ORMs (Prisma for Node/TS, SQLAlchemy for Python) rather than raw SQL by default.
* **Maintenance:** Enforce versioned, tracked schema migrations. Do not edit DBs manually.
* **Operations:** Schedule automated backups and conduct regular restore drills.
* **Security:** Apply least-privilege DB access (app user ≠ admin user).

## 7. Quality Assurance & Testing
* **Strategy:** Shift-Left testing via Git hooks. Maintain quality gates (minimum coverage + zero high-severity issues). Utilize AI coding assistants for automated unit test generation on isolated functions.
* **Test Types:**
  * **Unit Tests:** `Vitest`, `Jest`, `Pytest`.
  * **Integration Tests:** API and DB boundaries.
  * **E2E Automation:** `Playwright` or `Cypress` for critical user flows across viewports.
* **Data:** Implement reproducible test data seed scripts ensuring staging environment parity.

## 8. CI/CD & Deployment
* **Pipeline Pipeline (GitHub Actions / GitLab CI):** Build → Lint/Format → Run Tests → Security Scans (SAST + SCA) → Build/Containerize → Deploy.
* **Deployment Models:** Package apps into standard Docker containers to ensure environmental parity. Utilize atomic deployments (blue/green, zero-downtime rolling).
* **Release Management:** Segregate dev/staging/prod channels. Use feature flags for risky changes. Document release checklists and production rollback plans.
* **Hosting Configurations:** VPS (Hetzner, DigitalOcean) with Docker Compose for cost-efficiency, Vercel/Netlify for zero-config frontends, or Coolify for self-hosted PaaS.

## 9. Observability, Monitoring & Performance
* **Logging & Error Tracking:** Implement structured logging (`Winston`, `Pino`) and real-time exception tracking (`Sentry`, `Datadog`) for runtime errors and memory leaks.
* **Distributed Tracing & Metrics:** Implement OpenTelemetry to trace requests across frontend, API, and DB layers. Track RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) metrics.
* **Monitoring:** Use `UptimeRobot` or `Better Uptime`. Configure dashboards and alerts mapped to SLOs (e.g., 99.9% availability, p95 latency).
* **Performance Control:** Conduct load testing for critical endpoints. Review database indices. Implement Caching/CDNs, image optimization, and async job queues. Set budget alarms and cost allocation tags.

## 10. Compliance & Data Privacy
* **Minimization:** Collect only strictly necessary data. Document data inventory (PII collected, reasoning, retention periods).
* **Lifecycle:** Implement automated DB scripts to obfuscate or delete inactive data after legal thresholds.
* **Consent:** Build user preference centers for granular opt-out controls mapping to global privacy frameworks. Provide mechanisms for data export and deletion. Access controls + audit logs for sensitive data.

## 11. Maintenance, Operations & Support
* **System Health:** Schedule weekly dependency security patches and regular tech debt prioritization. Define EOL policies for outdated application or API versions. Archive old data/cleanup databases. Periodically rotate secrets.
* **Operations:** Establish ticket intake triage rules, escalation paths, and on-call rotations. Manage incidents via defined severity levels, postmortems, action items, and status page updates.

## 12. Documentation & Project Management
* **Living Documentation:** Maintain `README.md` (setup, run commands, tests), environment/config references, Runbooks (deploy, scale, rotate keys, restore DBs), ADR indices, and user FAQs.
* **Code Comments:** Restrict to non-obvious logic only.
* **AI Tooling:** Utilize LLM integrations to maintain dynamically updated context in the monorepo.
* **Task Management:** Standardize on Linear, GitHub Issues, or Plane (open-source) to track bugs, progress, and blockers.

## 13. Context & Agent Memory Guardrails
* **Context Pruning:** Exclude temporary builds, transient output directories, or artifact screenshots from main historical context loops.
* **Targeting:** Restrict historical analysis strictly to the current working tree when generating tools or executing refactors. Focus on explicit file inputs.

## Setup Priority Order
`Version Control → Env Management → Security → CI/CD → Testing → Monitoring → Docs → Maintenance`
