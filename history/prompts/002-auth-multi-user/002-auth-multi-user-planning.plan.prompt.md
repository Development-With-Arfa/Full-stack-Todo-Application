---
id: 002
title: Auth Multi-User Planning
stage: plan
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: 002-auth-multi-user
branch: 002-auth-multi-user
user: system
command: /sp.plan
labels: ["authentication", "jwt", "better-auth", "multi-user", "security", "planning"]
links:
  spec: specs/002-auth-multi-user/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-auth-multi-user/plan.md
  - specs/002-auth-multi-user/research.md
  - specs/002-auth-multi-user/data-model.md
  - specs/002-auth-multi-user/quickstart.md
  - specs/002-auth-multi-user/contracts/auth-api.yaml
  - specs/002-auth-multi-user/contracts/tasks-api.yaml
tests:
  - N/A (planning phase, no tests written)
---

## Prompt

/sp.plan

Spec 2: Authentication + Secure Multi-User Task Isolation
(Todo Full-Stack Web Application — Phase 2 Hackathon)

Create:
- Architecture sketch
- Implementation structure
- Security approach
- Quality validation

Decisions needing documentation:
- Key authentication + JWT design choices with tradeoffs

Testing strategy:
- Validation checks mapped to acceptance criteria

Organize by phases:
Research → Foundation → JWT Integration → Ownership Enforcement → Validation

[Full user input included architecture sketch, module structure, development approach, decisions, and testing strategy]

## Response snapshot

Successfully completed Phase 0 (Research) and Phase 1 (Design & Contracts) of the implementation planning workflow.

**Phase 0: Research & Discovery**
- Dispatched 3 parallel research agents to investigate:
  1. FastAPI JWT verification best practices (PyJWT vs python-jose)
  2. SQLModel foreign key patterns and migration strategies
  3. Better Auth JWT plugin configuration and token structure

Key findings:
- Better Auth uses asymmetric cryptography (EdDSA with Ed25519) by default, not shared secrets
- Backend should use PyJWT with PyJWKClient to fetch public keys from JWKS endpoint
- Dependency injection pattern recommended for FastAPI auth
- CASCADE delete configured for user-task relationship

**Phase 1: Design & Contracts**
Created comprehensive design artifacts:
1. **data-model.md**: Complete entity definitions (User, Task, Token), relationships, validation rules, migration strategy, and query patterns
2. **contracts/auth-api.yaml**: OpenAPI spec for Better Auth endpoints (sign-up, sign-in, sign-out, token, jwks)
3. **contracts/tasks-api.yaml**: OpenAPI spec for protected task endpoints with JWT authentication
4. **quickstart.md**: Step-by-step setup guide for both backend and frontend with code examples
5. **Agent context updated**: Added new technologies to CLAUDE.md

**Architecture Decisions Documented**:
1. JWT Verification Approach: Direct verification with JWKS endpoint (stateless)
2. User Identity Source: Always extract user_id from verified JWT claims
3. Authentication Enforcement: Dependency injection per route
4. Token Expiry: 24-hour default with Better Auth
5. Session Persistence: HTTP-only cookies (Better Auth default)

**Constitution Check**: ✅ PASSED - All requirements align with project principles

## Outcome

- ✅ Impact: Complete implementation plan with architecture decisions, research findings, data model, API contracts, and quickstart guide ready for task generation phase
- 🧪 Tests: Testing strategy defined in plan.md with multi-user isolation scenarios, JWT verification tests, and ownership enforcement tests
- 📁 Files: 6 design artifacts created (plan.md, research.md, data-model.md, quickstart.md, 2 OpenAPI specs)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed implementation tasks with acceptance criteria
- 🧠 Reflection: Research phase revealed that Better Auth uses asymmetric cryptography (not shared secrets), which is more secure and simplifies key management. The JWKS endpoint approach eliminates the need for secret sharing between frontend and backend.

## Evaluation notes (flywheel)

- Failure modes observed: None - all research agents completed successfully, all design artifacts generated
- Graders run and results (PASS/FAIL): Constitution Check: PASS, Research Completeness: PASS, Design Artifacts: PASS
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Proceed to /sp.tasks for task generation, then implementation phase
