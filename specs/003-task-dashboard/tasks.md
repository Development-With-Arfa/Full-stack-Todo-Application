---
description: "Implementation tasks for responsive task dashboard feature"
---

# Tasks: Responsive Task Dashboard

**Input**: Design documents from `/specs/003-task-dashboard/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not requested in specification - manual testing only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
- **Backend**: No changes required (existing from Feature 002)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and component structure

- [x] T001 Create components directory at frontend/components/
- [x] T002 [P] Create empty component files: frontend/components/LoadingSpinner.tsx, frontend/components/EmptyState.tsx, frontend/components/TaskForm.tsx, frontend/components/TaskCard.tsx, frontend/components/TaskList.tsx
- [x] T003 [P] Update frontend/lib/types.ts with TaskCardProps, TaskFormProps, TaskListProps, EmptyStateProps, LoadingSpinnerProps interfaces from data-model.md
- [x] T004 Create tasks page directory at frontend/app/tasks/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Verify authenticatedFetch wrapper works with GET /api/v1/tasks endpoint in frontend/lib/api-client.ts
- [x] T006 Verify Better Auth authentication guard pattern from existing auth pages in frontend/app/auth/signin/page.tsx
- [x] T007 Test JWT token attachment and 401 redirect behavior with authenticatedFetch

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View My Tasks (Priority: P1) 🎯 MVP

**Goal**: Display user's task list in a responsive dashboard with loading and empty states

**Independent Test**: User signs in and immediately sees their task list. Can be tested by creating tasks via API and verifying they appear in the dashboard.

### Implementation for User Story 1

- [x] T008 [P] [US1] Implement LoadingSpinner component in frontend/components/LoadingSpinner.tsx with size prop (sm, md, lg) and Tailwind animate-spin
- [x] T009 [P] [US1] Implement EmptyState component in frontend/components/EmptyState.tsx with message prop and centered layout
- [x] T010 [P] [US1] Implement TaskCard component (display mode only) in frontend/components/TaskCard.tsx showing title, description, completion status, and creation date
- [x] T011 [US1] Implement TaskList component in frontend/components/TaskList.tsx that renders TaskCard array or EmptyState with responsive grid layout (mobile: stacked, tablet: 2-col, desktop: 3-col)
- [x] T012 [US1] Create TasksPage in frontend/app/tasks/page.tsx with "use client" directive, authentication guard (redirect to /auth/signin if not authenticated), and state management (tasks, loading, error)
- [x] T013 [US1] Implement loadTasks function in frontend/app/tasks/page.tsx using authenticatedFetch GET /api/v1/tasks
- [x] T014 [US1] Add useEffect hook to fetch tasks on mount in frontend/app/tasks/page.tsx
- [x] T015 [US1] Integrate TaskList component into TasksPage with loading and error states in frontend/app/tasks/page.tsx
- [x] T016 [US1] Add responsive Tailwind classes to TaskList for mobile-first layout (space-y-4 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-4)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can view their tasks in a responsive dashboard

---

## Phase 4: User Story 2 - Create New Tasks (Priority: P1)

**Goal**: Add new task functionality with inline form and validation

**Independent Test**: User clicks "Add Task" button, fills in title and optional description, submits, and sees the new task appear immediately in the list.

### Implementation for User Story 2

- [x] T017 [US2] Implement TaskForm component (create mode) in frontend/components/TaskForm.tsx with controlled inputs for title and description, validation (title required, max 255 chars), and onSubmit prop
- [x] T018 [US2] Add form state management to TaskForm in frontend/components/TaskForm.tsx (title, description, errors) with useState hooks
- [x] T019 [US2] Implement client-side validation in TaskForm in frontend/components/TaskForm.tsx (title required, max lengths) with inline error display
- [x] T020 [US2] Add TaskForm component to TasksPage in frontend/app/tasks/page.tsx above TaskList with mode="create"
- [x] T021 [US2] Implement handleCreateTask function in frontend/app/tasks/page.tsx using authenticatedFetch POST /api/v1/tasks
- [x] T022 [US2] Add isCreating state and loading indicator to TaskForm in frontend/app/tasks/page.tsx
- [x] T023 [US2] Update tasks state to prepend new task to list after successful creation in frontend/app/tasks/page.tsx
- [x] T024 [US2] Add error handling for creation failures with user-friendly messages in frontend/app/tasks/page.tsx
- [x] T025 [US2] Implement form reset after successful task creation in frontend/components/TaskForm.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can view and create tasks

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P1)

**Goal**: Toggle task completion status with immediate visual feedback and optimistic updates

**Independent Test**: User clicks checkbox on a task to toggle completion status. The change is immediately visible and persists after page refresh.

### Implementation for User Story 3

- [x] T026 [US3] Add checkbox input to TaskCard component in frontend/components/TaskCard.tsx with checked state bound to task.completed
- [x] T027 [US3] Add visual styling for completed tasks in frontend/components/TaskCard.tsx (strikethrough title with line-through, muted text color with text-gray-500)
- [x] T028 [US3] Implement handleToggleComplete function in frontend/app/tasks/page.tsx using authenticatedFetch PUT /api/v1/tasks/{id} with completed field
- [x] T029 [US3] Add optimistic update logic in frontend/app/tasks/page.tsx (immediately update task.completed in state before API call)
- [x] T030 [US3] Implement error rollback in frontend/app/tasks/page.tsx (revert optimistic update if API call fails)
- [x] T031 [US3] Pass onToggle callback from TasksPage to TaskList to TaskCard in frontend/app/tasks/page.tsx and frontend/components/TaskList.tsx
- [x] T032 [US3] Add keyboard support for checkbox (Space key) with proper focus indicators in frontend/components/TaskCard.tsx
- [x] T033 [US3] Add aria-label to checkbox for screen reader accessibility in frontend/components/TaskCard.tsx

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - users can view, create, and toggle completion

---

## Phase 6: User Story 4 - Edit Existing Tasks (Priority: P2)

**Goal**: Update task details with inline editing and validation

**Independent Test**: User clicks "Edit" on a task, modifies title or description, saves, and sees the updated information immediately.

### Implementation for User Story 4

- [x] T034 [US4] Add "Edit" button to TaskCard component in frontend/components/TaskCard.tsx with onClick handler
- [x] T035 [US4] Add isEditing prop to TaskCard component in frontend/components/TaskCard.tsx to control display vs edit mode
- [x] T036 [US4] Implement edit mode in TaskCard in frontend/components/TaskCard.tsx that shows TaskForm with initialData and mode="edit"
- [x] T037 [US4] Update TaskForm component to support edit mode in frontend/components/TaskForm.tsx (pre-populate fields with initialData, show "Save" and "Cancel" buttons)
- [x] T038 [US4] Add editingTaskId state to TasksPage in frontend/app/tasks/page.tsx to track which task is being edited
- [x] T039 [US4] Implement handleEditTask function in frontend/app/tasks/page.tsx using authenticatedFetch PUT /api/v1/tasks/{id}
- [x] T040 [US4] Update tasks state to replace edited task after successful save in frontend/app/tasks/page.tsx
- [x] T041 [US4] Implement cancel functionality in TaskForm that calls onCancel prop in frontend/components/TaskForm.tsx
- [x] T042 [US4] Pass editingTaskId and onEditingChange callbacks through TaskList to TaskCard in frontend/app/tasks/page.tsx and frontend/components/TaskList.tsx
- [x] T043 [US4] Add error handling for edit failures with user-friendly messages in frontend/app/tasks/page.tsx

**Checkpoint**: At this point, User Stories 1-4 should all work - users can view, create, toggle, and edit tasks

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Remove tasks with confirmation dialog to prevent accidental deletion

**Independent Test**: User clicks "Delete" on a task, confirms the action, and the task is immediately removed from the list.

### Implementation for User Story 5

- [x] T044 [US5] Add "Delete" button to TaskCard component in frontend/components/TaskCard.tsx with onClick handler
- [x] T045 [US5] Implement confirmation dialog using browser confirm() in TaskCard onClick handler in frontend/components/TaskCard.tsx
- [x] T046 [US5] Implement handleDeleteTask function in frontend/app/tasks/page.tsx using authenticatedFetch DELETE /api/v1/tasks/{id}
- [x] T047 [US5] Update tasks state to filter out deleted task after successful deletion in frontend/app/tasks/page.tsx
- [x] T048 [US5] Pass onDelete callback from TasksPage to TaskList to TaskCard in frontend/app/tasks/page.tsx and frontend/components/TaskList.tsx
- [x] T049 [US5] Add error handling for deletion failures with user-friendly messages in frontend/app/tasks/page.tsx
- [x] T050 [US5] Add aria-label to delete button for screen reader accessibility in frontend/components/TaskCard.tsx

**Checkpoint**: All user stories (1-5) should now be independently functional - complete CRUD operations available

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure production readiness

- [x] T051 [P] Refine responsive layouts for all breakpoints (320px, 768px, 1024px+) across all components in frontend/components/
- [x] T052 [P] Add focus indicators (focus:ring-2 focus:ring-blue-500) to all interactive elements in frontend/components/
- [x] T053 [P] Verify color contrast meets WCAG 2.1 Level AA (4.5:1 ratio) for all text in frontend/components/
- [ ] T054 Test keyboard navigation (Tab, Enter, Space) for all operations in frontend/app/tasks/page.tsx
- [ ] T055 Test with screen reader (NVDA or JAWS) to verify all functionality is accessible
- [x] T056 [P] Add loading states to all async operations (create, edit, delete, toggle) in frontend/app/tasks/page.tsx
- [x] T057 [P] Optimize performance for 100+ tasks (verify smooth scrolling and rendering) in frontend/components/TaskList.tsx
- [x] T058 Add error boundary for graceful error handling in frontend/app/tasks/page.tsx
- [x] T059 [P] Format dates in human-readable format (e.g., "2 days ago") in frontend/components/TaskCard.tsx
- [x] T060 Verify all error messages are user-friendly and actionable in frontend/app/tasks/page.tsx
- [ ] T061 Test multi-user isolation (sign in as different users, verify task separation)
- [ ] T062 Test authentication token expiration handling (verify redirect to sign-in)
- [ ] T063 Run manual testing checklist from specs/003-task-dashboard/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Builds on US1 components but independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Extends TaskCard from US1 but independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Reuses TaskForm from US2 but independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Extends TaskCard from US1 but independently testable

### Within Each User Story

- Components marked [P] can be built in parallel (different files)
- TasksPage integration tasks depend on component completion
- Error handling and polish tasks come after core functionality

### Parallel Opportunities

- **Phase 1**: T002 and T003 can run in parallel (different files)
- **Phase 3 (US1)**: T008, T009, T010 can run in parallel (different component files)
- **Phase 8**: T051, T052, T053, T056, T057, T059 can run in parallel (different concerns)

---

## Parallel Example: User Story 1

```bash
# Launch all base components for User Story 1 together:
Task T008: "Implement LoadingSpinner component in frontend/components/LoadingSpinner.tsx"
Task T009: "Implement EmptyState component in frontend/components/EmptyState.tsx"
Task T010: "Implement TaskCard component (display mode) in frontend/components/TaskCard.tsx"

# Then build container and page:
Task T011: "Implement TaskList component in frontend/components/TaskList.tsx"
Task T012: "Create TasksPage in frontend/app/tasks/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (View Tasks)
4. Complete Phase 4: User Story 2 (Create Tasks)
5. Complete Phase 5: User Story 3 (Toggle Completion)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo MVP with core functionality

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (View only)
3. Add User Story 2 → Test independently → Deploy/Demo (View + Create)
4. Add User Story 3 → Test independently → Deploy/Demo (View + Create + Toggle) 🎯 MVP
5. Add User Story 4 → Test independently → Deploy/Demo (+ Edit)
6. Add User Story 5 → Test independently → Deploy/Demo (+ Delete) ✅ Complete
7. Add Polish → Final production-ready release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (View Tasks)
   - Developer B: User Story 2 (Create Tasks) - can start components in parallel
   - Developer C: User Story 3 (Toggle Completion) - can start in parallel
3. After P1 stories complete:
   - Developer A: User Story 4 (Edit Tasks)
   - Developer B: User Story 5 (Delete Tasks)
   - Developer C: Polish & Accessibility
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 63
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 3 tasks
- Phase 3 (US1 - View Tasks): 9 tasks
- Phase 4 (US2 - Create Tasks): 9 tasks
- Phase 5 (US3 - Toggle Completion): 8 tasks
- Phase 6 (US4 - Edit Tasks): 10 tasks
- Phase 7 (US5 - Delete Tasks): 7 tasks
- Phase 8 (Polish): 13 tasks

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel

**MVP Scope** (Recommended): Phases 1-5 (User Stories 1-3) = 33 tasks
- Provides core value: View, Create, and Toggle completion
- Fully functional and deployable
- Can add US4 and US5 in subsequent iterations

**Independent Test Criteria**:
- US1: Sign in and see task list with responsive layout
- US2: Create task and see it appear in list immediately
- US3: Toggle completion and see visual feedback with persistence
- US4: Edit task and see changes saved
- US5: Delete task with confirmation and see it removed

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No automated tests requested - manual testing only
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks include exact file paths for clarity
- Follow existing patterns from Feature 002 (authentication, API client, error handling)
