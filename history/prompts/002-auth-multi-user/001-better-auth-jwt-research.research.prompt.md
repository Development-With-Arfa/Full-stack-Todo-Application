---
id: 001
title: Better Auth JWT Integration Research
stage: research
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: 002-auth-multi-user
branch: 002-auth-multi-user
user: DELL
command: research
labels: ["authentication", "jwt", "better-auth", "fastapi", "security", "research"]
links:
  spec: E:\Todo_App_II\specs\002-auth-multi-user\spec.md
  ticket: null
  adr: null
  pr: null
files:
  - E:\Todo_App_II\specs\002-auth-multi-user\research.md
tests:
  - None (research phase)
---

## Prompt

Research the following topics for Better Auth JWT integration:

1. How to enable JWT plugin in Better Auth for Next.js
2. JWT token structure and claims issued by Better Auth
3. Shared secret configuration between frontend and backend

Focus on:
- Official Better Auth documentation for JWT plugin
- Configuration examples
- Token payload structure
- Best practices for secret sharing

Provide concrete findings with code examples where applicable.

## Response snapshot

Completed comprehensive research on Better Auth JWT integration with FastAPI backend. Key findings:

**1. Better Auth JWT Plugin Configuration**
- Installed via `better-auth` npm package with `jwt()` plugin
- Requires database migration to create `jwks` table for key storage
- Default algorithm: EdDSA with Ed25519 curve (asymmetric cryptography)
- Configurable payload, issuer, audience, expiration (default 15 minutes)

**2. JWT Token Structure**
- Header: Contains algorithm and key ID (kid)
- Payload: User data + standard claims (iss, aud, exp, sub)
- Signature: Cryptographically signed with private key
- Custom payload configuration available via `definePayload` function

**3. Shared Secret Configuration - CRITICAL FINDING**
- Better Auth uses **asymmetric cryptography** (public/private keys), NOT shared secrets
- Backend verifies tokens using public key from JWKS endpoint (`/api/auth/jwks`)
- No secret sharing needed - only public key is exposed (secure by design)
- PyJWT's `PyJWKClient` handles automatic key fetching and caching

**4. FastAPI JWT Verification**
- Recommendation: Use PyJWT (not python-jose) for better JWKS support
- Implementation pattern: Dependency injection with `Depends(get_current_user)`
- Verification includes: signature, expiration, issuer, audience validation
- User identity extracted from verified token claims (prevents impersonation)

**5. Database Relationships**
- SQLModel foreign key pattern: `user_id: int = Field(foreign_key="users.id")`
- Recommendation: CASCADE delete for automatic task cleanup
- Migration strategy documented for adding user_id to existing tasks

**6. Token Storage**
- Better Auth default: HTTP-only cookies (XSS protection)
- JWT retrieved on-demand for API calls via client plugin
- CORS configuration required for Authorization header

**7. Testing Strategy**
- pytest fixtures for multi-user scenarios
- Mock authentication for frontend tests
- End-to-end testing with multiple browser contexts
- Task isolation tests to verify 100% ownership enforcement

Created comprehensive research.md document with:
- Code examples for all components
- Architecture decision rationale
- Implementation checklist
- Security best practices
- Multi-user testing patterns

## Outcome

- ✅ Impact: Resolved all technical unknowns for Phase 0 research. Established clear implementation patterns for JWT authentication with Better Auth and FastAPI. Critical discovery: asymmetric cryptography eliminates need for shared secret management.
- 🧪 Tests: No tests run (research phase). Documented testing strategy for implementation phase including multi-user isolation tests, JWT verification tests, and E2E scenarios.
- 📁 Files: Created 1 file - specs/002-auth-multi-user/research.md (comprehensive 500+ line research document with code examples)
- 🔁 Next prompts: Phase 1 design work - create data-model.md, API contracts (contracts/), and quickstart.md. Then proceed to /sp.tasks for Phase 2 task generation.
- 🧠 Reflection: Research revealed that Better Auth's asymmetric approach is more secure than initially assumed shared secret pattern. JWKS endpoint pattern is industry standard and well-supported by PyJWT. All constitutional requirements can be met with documented patterns.

## Evaluation notes (flywheel)

- Failure modes observed: Initial web search API errors required fallback to direct WebFetch. Python backend context required adjustment from initial Next.js-only assumption.
- Graders run and results (PASS/FAIL): N/A (research phase)
- Prompt variant (if applicable): Standard research prompt with specific focus areas
- Next experiment (smallest change to try): Proceed with Phase 1 design (data-model.md) to validate research findings against actual schema design. Test PyJWT JWKS integration with Better Auth in development environment.
