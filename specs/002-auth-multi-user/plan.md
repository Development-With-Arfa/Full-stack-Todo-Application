# Implementation Plan: Authentication and Secure Multi-User Task Isolation

**Branch**: `002-auth-multi-user` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-auth-multi-user/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate Better Auth in the Next.js frontend to handle user registration and sign-in with JWT token issuance. Implement JWT verification in the FastAPI backend to authenticate all task API requests. Enforce strict user ownership on all task operations so that each user can only access, create, update, and delete their own tasks. Update the existing task CRUD functionality to include user_id associations and filter all queries by the authenticated user.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript/JavaScript (Frontend with Next.js 16+)
**Primary Dependencies**:
- Frontend: Next.js 16+ (App Router), Better Auth with JWT plugin, React
- Backend: FastAPI, SQLModel, PyJWT, python-jose
**Storage**: Neon Serverless PostgreSQL (existing, needs user table + user_id foreign key on tasks)
**Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Web application (Linux server for backend, modern browsers for frontend)
**Project Type**: Web (frontend + backend)
**Performance Goals**:
- Authentication token validation < 50ms latency per request
- Support 100+ concurrent authenticated users
- Sign-in/sign-up completion < 10 seconds
**Constraints**:
- 100% task isolation (zero cross-user access)
- JWT tokens must be cryptographically verified
- All task endpoints must require authentication
- Shared secret between Better Auth and FastAPI for JWT verification
**Scale/Scope**:
- Multi-user system (100+ users for hackathon demo)
- Existing task CRUD endpoints to be protected
- 2 new auth pages (sign-in, sign-up)
- 4-6 backend security modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **Secure Multi-User Task Isolation and Ownership Enforcement**
- Plan includes JWT authentication on all task endpoints
- User ID extraction from verified tokens
- Database queries filtered by authenticated user_id
- Authorization checks before any task operation

✅ **Reliable Backend Persistence with Neon PostgreSQL**
- Existing Neon PostgreSQL database will be extended with users table
- SQLModel ORM will handle user-task relationships
- Foreign key constraints for data integrity

✅ **Clear Separation of Frontend, Backend, and Authentication Layers**
- Better Auth handles authentication in Next.js frontend
- FastAPI backend independently verifies JWT tokens
- Clear API contract with Authorization: Bearer <token> header
- No authentication logic mixed with business logic

✅ **Production-Grade REST API Design and Validation**
- Existing RESTful task endpoints maintained
- Proper HTTP status codes (401 Unauthorized, 403 Forbidden)
- JWT validation middleware as reusable dependency

✅ **Consistent JWT Authentication and Authorization**
- Better Auth JWT plugin for token issuance
- Shared secret (BETTER_AUTH_SECRET) for signature verification
- Middleware/dependency injection for consistent auth enforcement

✅ **Responsive and Accessible Frontend UI**
- Sign-in and sign-up pages follow existing UI patterns
- Form validation and error messaging
- Responsive design maintained

### Technology Stack Compliance

✅ **Frontend**: Next.js 16+ (App Router) - compliant
✅ **Backend**: Python FastAPI - compliant
✅ **ORM**: SQLModel - compliant
✅ **Database**: Neon Serverless PostgreSQL - compliant
✅ **Authentication**: Better Auth with JWT plugin - compliant

**Gate Status**: ✅ PASSED - All constitutional requirements met

## Project Structure

### Documentation (this feature)

```text
specs/002-auth-multi-user/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   ├── auth-api.yaml    # Better Auth endpoints
│   └── tasks-api.yaml   # Updated task endpoints with auth
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── core/
│   │   ├── config.py           # Environment config (BETTER_AUTH_SECRET)
│   │   └── security.py         # JWT decode + verification utilities (NEW)
│   ├── middleware/
│   │   └── auth.py             # Auth dependency for route protection (NEW)
│   ├── models/
│   │   ├── task.py             # Task model (UPDATE: add user_id FK)
│   │   └── user.py             # User model (NEW)
│   ├── routes/
│   │   ├── auth.py             # Auth routes if needed (NEW)
│   │   └── tasks.py            # Task routes (UPDATE: add auth dependency)
│   ├── services/
│   │   ├── task_service.py     # Task business logic (UPDATE: filter by user_id)
│   │   └── user_service.py     # User business logic (NEW)
│   └── main.py                 # FastAPI app (UPDATE: add auth middleware)
└── tests/
    ├── test_auth.py            # Auth tests (NEW)
    ├── test_security.py        # JWT verification tests (NEW)
    └── test_tasks.py           # Task tests (UPDATE: multi-user scenarios)

frontend/
├── app/
│   ├── auth/
│   │   ├── signin/
│   │   │   └── page.tsx        # Sign-in page (NEW)
│   │   └── signup/
│   │       └── page.tsx        # Sign-up page (NEW)
│   ├── tasks/
│   │   └── page.tsx            # Task dashboard (UPDATE: auth-protected)
│   └── layout.tsx              # Root layout (UPDATE: auth provider)
├── lib/
│   ├── auth.ts                 # Better Auth config + JWT plugin (NEW)
│   └── apiClient.ts            # Fetch wrapper with JWT attachment (NEW)
└── components/
    ├── AuthGuard.tsx           # Client-side auth guard (NEW)
    └── SignOutButton.tsx       # Sign-out button (NEW)
```

**Structure Decision**: Web application structure with separate frontend and backend directories. Frontend uses Next.js App Router with Better Auth integration. Backend uses FastAPI with modular structure separating security, models, routes, and services. This aligns with the constitutional requirement for clear separation of layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All requirements align with constitutional principles.

## Phase 0: Research & Discovery

**Objective**: Resolve all technical unknowns and establish implementation patterns.

### Research Tasks

1. **Better Auth JWT Plugin Configuration**
   - Research: How to enable JWT plugin in Better Auth for Next.js
   - Research: JWT token structure and claims issued by Better Auth
   - Research: Shared secret configuration between frontend and backend

2. **FastAPI JWT Verification**
   - Research: Best practices for JWT verification in FastAPI
   - Research: PyJWT vs python-jose library comparison
   - Research: Dependency injection pattern for auth in FastAPI

3. **User-Task Database Relationship**
   - Research: SQLModel foreign key patterns
   - Research: Migration strategy for adding user_id to existing tasks table
   - Research: Cascading delete behavior for user-task relationship

4. **Token Storage and Transmission**
   - Research: HTTP-only cookies vs localStorage for JWT storage
   - Research: CORS configuration for Authorization header
   - Research: Token refresh strategy (if needed for hackathon scope)

5. **Multi-User Testing Strategy**
   - Research: pytest fixtures for multi-user scenarios
   - Research: Frontend testing with mocked authentication
   - Research: End-to-end testing with multiple authenticated sessions

**Output**: `research.md` with findings and decisions for each research task

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

### 1.1 Data Model Design

**Output**: `data-model.md`

**Entities**:
- User (new)
- Task (updated with user_id foreign key)
- Authentication Token (transient, not stored)

**Relationships**:
- User 1:N Task (one user owns many tasks)

**Validation Rules**:
- User email must be unique and valid format
- User password must meet strength requirements (min 8 chars, letter + number)
- Task user_id must reference existing user
- All task queries must filter by authenticated user_id

### 1.2 API Contracts

**Output**: `contracts/` directory with OpenAPI specs

**New Endpoints**:
- POST /auth/signup - User registration
- POST /auth/signin - User sign-in
- POST /auth/signout - User sign-out

**Updated Endpoints** (all require Authorization: Bearer <token>):
- GET /tasks - List tasks (filtered by authenticated user)
- POST /tasks - Create task (associated with authenticated user)
- GET /tasks/{id} - Get task (ownership verified)
- PUT /tasks/{id} - Update task (ownership verified)
- DELETE /tasks/{id} - Delete task (ownership verified)

**Authentication Flow**:
1. Client calls Better Auth sign-in endpoint
2. Better Auth returns JWT token
3. Client includes token in Authorization header for all task API calls
4. FastAPI verifies token and extracts user_id
5. FastAPI filters/validates operations by user_id

### 1.3 Quickstart Guide

**Output**: `quickstart.md`

**Setup Steps**:
1. Configure BETTER_AUTH_SECRET in both frontend and backend .env
2. Run database migration to add users table and user_id to tasks
3. Install Better Auth dependencies in frontend
4. Install PyJWT/python-jose in backend
5. Start both frontend and backend servers
6. Test sign-up, sign-in, and task isolation

### 1.4 Agent Context Update

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Technologies to Add**:
- Better Auth (authentication framework)
- JWT (JSON Web Tokens)
- PyJWT or python-jose (JWT verification library)

## Phase 2: Task Generation

**Note**: Phase 2 is handled by the `/sp.tasks` command, not `/sp.plan`.

The `/sp.tasks` command will generate `tasks.md` with:
- Testable implementation tasks
- Acceptance criteria mapped to spec requirements
- Dependency ordering (auth setup → backend verification → ownership enforcement)
- Test cases for multi-user scenarios

## Architecture Decisions Requiring Documentation

### Decision 1: JWT Verification Approach

**Context**: Backend needs to verify JWT tokens issued by Better Auth frontend.

**Options Considered**:
- **Option A**: Verify JWT directly in FastAPI using shared secret (stateless)
- **Option B**: Backend calls frontend session API for verification (stateful)

**Decision**: Option A - Direct JWT verification with shared secret

**Rationale**:
- Stateless verification is faster and more scalable
- No coupling between backend and frontend session management
- Standard JWT verification pattern
- Reduces network overhead (no additional API call per request)

**Tradeoffs**:
- Requires secure sharing of BETTER_AUTH_SECRET between services
- Cannot revoke tokens before expiration (acceptable for hackathon scope)

### Decision 2: User Identity Source

**Context**: Backend needs to identify which user is making the request.

**Options Considered**:
- **Option A**: Extract user_id from verified JWT claims (secure)
- **Option B**: Accept user_id from URL parameter or request body (unsafe)

**Decision**: Option A - Always derive user_id from JWT token claims

**Rationale**:
- Prevents user impersonation attacks
- Token signature guarantees authenticity of user_id
- Aligns with zero-trust security model

**Tradeoffs**:
- None - this is the only secure approach

### Decision 3: Authentication Enforcement Pattern

**Context**: All task endpoints must require authentication.

**Options Considered**:
- **Option A**: Global middleware that protects all routes
- **Option B**: Dependency injection per route (FastAPI Depends)

**Decision**: Option B - Dependency injection for route-level control

**Rationale**:
- Explicit authentication requirement visible in route definition
- Allows flexibility for public endpoints if needed later
- FastAPI best practice for reusable dependencies
- Easier to test individual routes

**Tradeoffs**:
- Must remember to add dependency to each protected route
- Slightly more verbose than global middleware

### Decision 4: Token Expiry Handling

**Context**: JWT tokens have expiration time; need to handle expired tokens.

**Options Considered**:
- **Option A**: Short expiry (1 hour) with refresh token mechanism
- **Option B**: Longer expiry (24 hours) with Better Auth default
- **Option C**: Very long expiry (7 days) for convenience

**Decision**: Option B - Use Better Auth default session expiry (24 hours)

**Rationale**:
- Balances security and user experience for hackathon scope
- Leverages Better Auth's built-in session management
- Reduces implementation complexity (no refresh token flow needed)
- Users can stay signed in for a full day of demo usage

**Tradeoffs**:
- Less secure than short-lived tokens with refresh
- Acceptable for hackathon/demo environment

### Decision 5: Session Persistence Strategy

**Context**: Users expect to remain signed in across browser refreshes.

**Options Considered**:
- **Option A**: HTTP-only cookies (more secure)
- **Option B**: localStorage (easier to implement)
- **Option C**: sessionStorage (cleared on browser close)

**Decision**: Defer to Better Auth default (likely HTTP-only cookies)

**Rationale**:
- Better Auth handles token storage automatically
- HTTP-only cookies prevent XSS attacks
- Follows security best practices
- No custom implementation needed

**Tradeoffs**:
- Less control over storage mechanism
- Acceptable given Better Auth's security focus

## Testing Strategy

### Authentication Tests

**Signup Flow**:
- ✅ Valid credentials create user account
- ✅ Duplicate email returns error
- ✅ Weak password rejected
- ✅ Invalid email format rejected

**Signin Flow**:
- ✅ Valid credentials return JWT token
- ✅ Invalid credentials return 401
- ✅ Missing credentials return 400
- ✅ Token contains correct user_id claim

**Signout Flow**:
- ✅ Signout invalidates session
- ✅ Subsequent requests with old token fail

### JWT Verification Tests

**Token Validation**:
- ✅ Valid token with correct signature passes
- ✅ Invalid signature rejected
- ✅ Expired token rejected
- ✅ Malformed token rejected
- ✅ Missing token returns 401
- ✅ Token with wrong secret rejected

**User Extraction**:
- ✅ user_id correctly extracted from token claims
- ✅ Invalid user_id in token rejected

### Ownership Enforcement Tests

**Task Isolation**:
- ✅ User A creates task → User B cannot see it
- ✅ User A creates task → User B cannot update it
- ✅ User A creates task → User B cannot delete it
- ✅ User A lists tasks → only sees own tasks
- ✅ User B lists tasks → only sees own tasks

**Authorization Checks**:
- ✅ GET /tasks/{id} with wrong owner returns 403
- ✅ PUT /tasks/{id} with wrong owner returns 403
- ✅ DELETE /tasks/{id} with wrong owner returns 403
- ✅ Non-existent task returns 404 (not 403 to avoid info leak)

**Edge Cases**:
- ✅ Unauthenticated request to any task endpoint returns 401
- ✅ Token expires mid-session → graceful re-auth prompt
- ✅ Concurrent requests from same user handled correctly
- ✅ Task ID guessing attack prevented

### API Security Validation

**Endpoint Protection**:
- ✅ All task endpoints require valid JWT
- ✅ No endpoint allows cross-user access
- ✅ Proper HTTP status codes returned
- ✅ Error messages don't leak sensitive info

**Integration Tests**:
- ✅ End-to-end signup → signin → create task → signout flow
- ✅ Multi-user scenario: User A and B operate independently
- ✅ Token refresh/expiry handling (if implemented)

## Deliverable Outcome

By completion of Phase 1 (this command):
- ✅ Implementation plan documented with architecture decisions
- ✅ Research findings consolidated in research.md
- ✅ Data model designed in data-model.md
- ✅ API contracts defined in contracts/
- ✅ Quickstart guide created in quickstart.md
- ✅ Agent context updated with new technologies

By completion of Phase 2 (/sp.tasks command):
- Detailed task breakdown with acceptance criteria
- Test cases mapped to functional requirements
- Implementation order with dependencies

By completion of implementation:
- Better Auth signup/signin working in Next.js
- JWT tokens issued and attached to API calls
- FastAPI verifies JWT and enforces user isolation
- 100% task isolation validated through testing
- Multi-user demo ready for hackathon evaluation
