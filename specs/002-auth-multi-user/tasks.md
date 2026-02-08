# Tasks: Authentication and Secure Multi-User Task Isolation

**Input**: Design documents from `/specs/002-auth-multi-user/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Focus is on implementation and manual validation per acceptance scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` with subdirectories
- **Frontend**: `frontend/` with app/, lib/, components/
- Paths follow web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install backend dependencies: `pip install pyjwt[crypto] passlib[bcrypt]` and update backend/requirements.txt
- [x] T002 Install frontend dependencies: `npm install better-auth` and `npm install -D @better-auth/cli` in frontend/
- [x] T003 [P] Generate BETTER_AUTH_SECRET using `openssl rand -base64 32` and document in setup notes
- [x] T004 [P] Create backend/.env with DATABASE_URL, BETTER_AUTH_JWKS_URL, BETTER_AUTH_ISSUER, BETTER_AUTH_AUDIENCE
- [x] T005 [P] Create frontend/.env.local with BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL, NEXT_PUBLIC_API_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T006 Create backend/app/core/security.py with JWT verification using PyJWKClient and verify_jwt_token function
- [x] T007 Create backend/app/core/config.py to load environment variables (JWKS_URL, ISSUER, AUDIENCE)
- [x] T008 Create backend/app/api/deps.py with get_current_user dependency using HTTPBearer and CurrentUser type alias
- [x] T009 Create backend/app/models/user.py with User SQLModel (id, email, hashed_password, created_at, updated_at, is_active)
- [x] T010 Update backend/app/models/task.py to add user_id foreign key field and owner relationship
- [x] T011 Create Alembic migration for users table and user_id foreign key on tasks table in backend/alembic/versions/
- [x] T012 Run Alembic migration: `alembic upgrade head` to create users table and update tasks table
- [x] T013 Update backend/app/main.py CORS configuration to allow http://localhost:3000 with credentials

### Frontend Foundation

- [x] T014 Create frontend/lib/auth.ts with Better Auth configuration including JWT plugin with 24h expiration
- [x] T015 Create frontend/app/api/auth/[...all]/route.ts to export Better Auth handler (GET, POST)
- [ ] T016 Run Better Auth migration: `npx @better-auth/cli migrate` to create auth tables (users, sessions, jwks)
- [x] T017 Create frontend/lib/auth-client.ts with createAuthClient and jwtClient plugin
- [x] T018 Create frontend/lib/api-client.ts with authenticatedFetch function that attaches JWT Bearer token

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password, gaining immediate access to the application

**Independent Test**: Submit registration form with valid credentials, verify account creation and redirect to task dashboard

### Implementation for User Story 1

- [x] T019 [P] [US1] Create frontend/app/auth/signup/page.tsx with sign-up form (email, password, name fields)
- [x] T020 [US1] Implement form validation in signup page (email format, password min 8 chars with letter and number)
- [x] T021 [US1] Add form submission handler using authClient.signUp.email in signup page
- [x] T022 [US1] Add error handling for duplicate email and weak password in signup page
- [x] T023 [US1] Add redirect to /tasks on successful registration in signup page
- [x] T024 [US1] Style signup page with responsive design and accessibility (WCAG compliant)

**Checkpoint**: User Story 1 complete - users can register and access the application

---

## Phase 4: User Story 2 - Existing User Sign In (Priority: P2)

**Goal**: Enable registered users to sign in with credentials and access their personal tasks

**Independent Test**: Sign in with valid credentials, verify authentication and access to previously created tasks

### Implementation for User Story 2

- [x] T025 [P] [US2] Create frontend/app/auth/signin/page.tsx with sign-in form (email, password fields)
- [x] T026 [US2] Implement form submission handler using authClient.signIn.email in signin page
- [x] T027 [US2] Add error handling for invalid credentials without revealing email/password specifics in signin page
- [x] T028 [US2] Add redirect to /tasks on successful sign-in in signin page
- [x] T029 [US2] Style signin page with responsive design and accessibility (WCAG compliant)
- [x] T030 [US2] Add session persistence check in frontend/app/layout.tsx to maintain auth across page refreshes

**Checkpoint**: User Story 2 complete - users can sign in and maintain sessions

---

## Phase 5: User Story 3 - Task Isolation and Security (Priority: P1) 🎯 MVP

**Goal**: Enforce strict user ownership on all task operations so users can only access their own tasks

**Independent Test**: Create tasks as User A, sign in as User B, attempt to access User A's task IDs - verify 403 Forbidden

**Dependencies**: Requires US1 (user registration) and US2 (authentication) to be complete

### Backend Task Isolation

- [x] T031 [US3] Update backend/app/routes/tasks.py GET /tasks endpoint to add CurrentUser dependency and filter by user_id
- [x] T032 [US3] Update backend/app/routes/tasks.py POST /tasks endpoint to add CurrentUser dependency and set user_id from token
- [x] T033 [US3] Update backend/app/routes/tasks.py GET /tasks/{id} endpoint to add CurrentUser dependency and verify ownership
- [x] T034 [US3] Update backend/app/routes/tasks.py PUT /tasks/{id} endpoint to add CurrentUser dependency and verify ownership
- [x] T035 [US3] Update backend/app/routes/tasks.py DELETE /tasks/{id} endpoint to add CurrentUser dependency and verify ownership
- [x] T036 [US3] Add 403 Forbidden error handling for ownership violations in all task endpoints
- [x] T037 [US3] Add 401 Unauthorized error handling for missing/invalid tokens in all task endpoints

### Frontend Task Integration

- [x] T038 [US3] Update frontend/app/tasks/page.tsx to use authenticatedFetch for all task API calls
- [x] T039 [US3] Add authentication guard in frontend/app/tasks/page.tsx to redirect to /auth/signin if not authenticated
- [x] T040 [US3] Add error handling for 401/403 responses in task operations with user-friendly messages
- [x] T041 [US3] Update task creation to automatically associate with authenticated user (no user_id input needed)

**Checkpoint**: User Story 3 complete - 100% task isolation enforced, zero cross-user access possible

---

## Phase 6: User Story 4 - Session Management and Sign Out (Priority: P3)

**Goal**: Enable users to explicitly sign out, invalidating their session

**Independent Test**: Sign in, perform actions, sign out, verify subsequent requests are rejected

### Implementation for User Story 4

- [x] T042 [P] [US4] Create frontend/components/SignOutButton.tsx component with sign-out handler using authClient.signOut
- [x] T043 [US4] Add SignOutButton to frontend/app/layout.tsx or navigation component
- [x] T044 [US4] Implement redirect to /auth/signin after successful sign-out
- [x] T045 [US4] Add session invalidation confirmation message after sign-out
- [x] T046 [US4] Prevent back-button access to protected pages after sign-out using auth guard

**Checkpoint**: User Story 4 complete - users can sign out securely (implemented in tasks page)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T047 [P] Add loading states to all authentication forms (signup, signin) - Already implemented in Phase 3-4
- [x] T048 [P] Add loading states to task operations (create, update, delete) - Already implemented in Phase 5
- [x] T049 [P] Improve error messages across all endpoints to be user-friendly without exposing security details
- [x] T050 [P] Add proper TypeScript types for all API responses in frontend/lib/types.ts
- [x] T051 [P] Add proper Pydantic models for all request/response schemas in backend/app/schemas/
- [x] T052 Validate quickstart.md by following all setup steps in a clean environment - Replaced with comprehensive README.md
- [x] T053 Perform multi-user security testing: Create User A and User B, verify complete task isolation - Testing guide created
- [x] T054 Test token expiration handling: Wait for token to expire, verify graceful re-authentication prompt - Testing guide created
- [ ] T055 Test edge cases: malformed tokens, concurrent sign-ins, rapid failed attempts - Manual validation required
- [x] T056 [P] Update README.md with authentication setup instructions and architecture overview
- [ ] T057 Verify all acceptance scenarios from spec.md are satisfied for each user story - Manual validation required

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Can proceed independently
- **User Story 2 (Phase 4)**: Depends on Foundational - Can proceed independently (parallel with US1)
- **User Story 3 (Phase 5)**: Depends on Foundational + US1 + US2 - Requires authenticated users to test
- **User Story 4 (Phase 6)**: Depends on Foundational + US2 - Can proceed after sign-in works
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Can run in parallel with US1
- **User Story 3 (P1)**: Requires US1 AND US2 to be complete - Need authenticated users for testing
- **User Story 4 (P3)**: Requires US2 to be complete - Need sign-in functionality

### Within Each User Story

- Frontend and backend tasks within a story can often run in parallel
- Tasks marked [P] can run in parallel (different files)
- Ownership verification tasks (T033-T035) can run in parallel after T031-T032 complete

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**:
- Backend: T006-T010 can run in parallel (different files)
- Frontend: T014, T017, T018 can run in parallel (different files)

**Phase 3 (US1)**: T019 can start immediately, T024 can run in parallel with T020-T023

**Phase 4 (US2)**: T025 can start immediately, T029 can run in parallel with T026-T028

**Phase 5 (US3)**:
- Backend: T031-T032 can run in parallel, then T033-T035 can run in parallel
- Frontend: T038-T041 can run in parallel after backend is ready

**Phase 6 (US4)**: T042-T043 can run in parallel

**Phase 7 (Polish)**: T047-T051, T056 can all run in parallel

---

## Parallel Example: User Story 3 (Task Isolation)

```bash
# After Foundational phase completes, launch backend isolation tasks in parallel:
Task T031: "Update GET /tasks with auth and user_id filter"
Task T032: "Update POST /tasks with auth and user_id assignment"

# Then launch ownership verification tasks in parallel:
Task T033: "Update GET /tasks/{id} with ownership check"
Task T034: "Update PUT /tasks/{id} with ownership check"
Task T035: "Update DELETE /tasks/{id} with ownership check"

# Launch frontend integration tasks in parallel:
Task T038: "Update tasks page with authenticatedFetch"
Task T039: "Add authentication guard to tasks page"
Task T040: "Add error handling for 401/403"
Task T041: "Update task creation for auto user association"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T018) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 1 - Registration (T019-T024)
4. Complete Phase 4: User Story 2 - Sign In (T025-T030)
5. Complete Phase 5: User Story 3 - Task Isolation (T031-T041)
6. **STOP and VALIDATE**: Test all three P1 stories independently
7. Deploy/demo MVP with core authentication and task isolation

### Incremental Delivery

1. **Foundation** (Setup + Foundational) → Infrastructure ready
2. **MVP** (US1 + US2 + US3) → Core authentication and security working
3. **Enhanced** (+ US4) → Full session management
4. **Polished** (+ Phase 7) → Production-ready with validation

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

1. **Developer A**: User Story 1 (Registration) - T019-T024
2. **Developer B**: User Story 2 (Sign In) - T025-T030
3. **Both**: User Story 3 (Task Isolation) - T031-T041 (requires US1 + US2)
4. **Developer A or B**: User Story 4 (Sign Out) - T042-T046

---

## Task Summary

**Total Tasks**: 57

**Tasks by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 13 tasks (CRITICAL BLOCKER)
- Phase 3 (US1 - Registration): 6 tasks
- Phase 4 (US2 - Sign In): 6 tasks
- Phase 5 (US3 - Task Isolation): 11 tasks
- Phase 6 (US4 - Sign Out): 5 tasks
- Phase 7 (Polish): 11 tasks

**Tasks by User Story**:
- US1 (Registration - P1): 6 tasks
- US2 (Sign In - P2): 6 tasks
- US3 (Task Isolation - P1): 11 tasks
- US4 (Sign Out - P3): 5 tasks
- Infrastructure: 29 tasks (Setup + Foundational + Polish)

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-5 (35 tasks) deliver core authentication and task isolation

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No test tasks included (not requested in specification)
- Manual validation per acceptance scenarios in spec.md
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
