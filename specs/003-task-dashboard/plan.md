# Implementation Plan: Responsive Task Dashboard

**Branch**: `003-task-dashboard` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-task-dashboard/spec.md`

## Summary

Build a responsive Next.js dashboard UI that provides complete task management functionality (view, create, edit, delete, toggle completion) with mobile-first design. The dashboard integrates with the existing FastAPI backend (Feature 002) using JWT authentication, ensuring all task operations are secure and user-isolated. The implementation focuses on a single-page dashboard with inline task creation and editing for optimal user experience.

**Primary Requirement**: Authenticated users can manage their tasks through a clean, responsive interface that works seamlessly on mobile and desktop devices.

**Technical Approach**: Extend the existing Next.js frontend with a new dashboard page (`/tasks`) that uses React state management and the existing authenticated API client to perform CRUD operations. All UI components will be built with Tailwind CSS for consistent styling and responsive behavior.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 16+ (App Router), React 18+
**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Tailwind CSS, Better Auth (existing)
- Backend: FastAPI (existing from Feature 002), SQLModel, PyJWT
**Storage**: Neon Serverless PostgreSQL (existing, accessed via FastAPI backend)
**Testing**: Manual testing following test guides (automated tests not in scope)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile devices
**Project Type**: Web application (frontend + backend already established)
**Performance Goals**:
- Page load < 2 seconds
- Task operations < 1 second
- Support 100+ tasks without degradation
**Constraints**:
- Must use existing authentication from Feature 002
- Must maintain user task isolation
- Mobile-first responsive design (320px - 1920px)
- Keyboard accessible (WCAG 2.1 Level AA)
**Scale/Scope**:
- Single dashboard page with 5 user stories
- 5 React components
- Integration with 5 existing API endpoints
- Support for unlimited tasks per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Secure Multi-User Task Isolation and Ownership Enforcement
**Status**: PASS - Dashboard will use existing authenticated API client from Feature 002 that automatically includes JWT tokens. All API calls respect user ownership enforced by backend.

### ✅ Reliable Backend Persistence with Neon PostgreSQL
**Status**: PASS - No changes to backend persistence layer. Dashboard uses existing FastAPI endpoints that persist to Neon PostgreSQL via SQLModel.

### ✅ Clear Separation of Frontend, Backend, and Authentication Layers
**Status**: PASS - Dashboard is pure frontend implementation. Uses existing API client (`lib/api-client.ts`) to communicate with backend. Authentication handled by existing Better Auth integration.

### ✅ Production-Grade REST API Design and Validation
**Status**: PASS - Dashboard consumes existing RESTful API endpoints from Feature 002. No new backend endpoints required (GET, POST, PUT, DELETE already exist).

### ✅ Consistent JWT Authentication and Authorization
**Status**: PASS - Dashboard uses existing `authenticatedFetch` wrapper that automatically attaches JWT Bearer tokens. Authentication guard redirects unauthenticated users to sign-in.

### ✅ Responsive and Accessible Frontend UI
**Status**: PASS - Dashboard will be built with Tailwind CSS responsive utilities. Keyboard navigation and WCAG 2.1 Level AA compliance are explicit requirements in spec.

### ✅ Technology Stack Constraints
**Status**: PASS - Uses Next.js 16+ App Router, React, Tailwind CSS, Better Auth (all existing). No new frameworks or libraries introduced.

### ✅ Development Standards
**Status**: PASS - Follows existing patterns from Feature 002 (authentication guards, error handling, API client usage). Consistent with established codebase conventions.

**Constitution Compliance**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/003-task-dashboard/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (architectural plan)
├── research.md          # Phase 0: Technical research and decisions
├── data-model.md        # Phase 1: Data structures and state management
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: Component interfaces and API contracts
│   ├── components.md    # Component prop interfaces
│   └── api-integration.md # API endpoint contracts
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── tasks/
│   │   └── page.tsx           # Main dashboard page (NEW)
│   ├── auth/                  # Existing authentication pages
│   └── layout.tsx             # Existing root layout
├── components/                # NEW directory for reusable components
│   ├── TaskList.tsx          # Task list container
│   ├── TaskCard.tsx          # Individual task display
│   ├── TaskForm.tsx          # Create/edit task form
│   ├── EmptyState.tsx        # No tasks message
│   └── LoadingSpinner.tsx    # Loading indicator
├── lib/
│   ├── api-client.ts         # Existing authenticated API client
│   ├── auth-client.ts        # Existing Better Auth client
│   └── types.ts              # Existing + NEW task types
└── public/                    # Static assets

backend/
├── src/
│   └── api/v1/endpoints/
│       └── tasks.py          # Existing task endpoints (no changes)
└── app/
    └── models/
        └── task.py           # Existing task model (no changes)
```

**Structure Decision**: Web application structure (Option 2) is already established. This feature adds only frontend components and pages. Backend infrastructure from Feature 002 remains unchanged. The dashboard integrates seamlessly with existing authentication and API layers.

## Complexity Tracking

> **No violations** - All constitution checks passed. This feature builds on existing infrastructure without introducing new complexity.

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User's Browser                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Dashboard Page (/tasks)                           │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  TaskList    │  │  TaskForm    │               │    │
│  │  │  Component   │  │  Component   │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  TaskCard    │  │  EmptyState  │               │    │
│  │  │  Component   │  │  Component   │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
│                          │ React State (useState)           │
│                          │                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  API Integration Layer                             │    │
│  │  - authenticatedFetch (existing)                   │    │
│  │  - Automatic JWT token attachment                  │    │
│  │  - Error handling                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │ HTTPS + JWT Bearer Token
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              FastAPI Backend (Feature 002)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐    │
│  │  Authentication Middleware                         │    │
│  │  - JWT verification via JWKS                       │    │
│  │  - User ID extraction                              │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Task API Endpoints (existing)                     │    │
│  │  - GET    /api/v1/tasks                            │    │
│  │  - POST   /api/v1/tasks                            │    │
│  │  - PUT    /api/v1/tasks/{id}                       │    │
│  │  - DELETE /api/v1/tasks/{id}                       │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  SQLModel ORM + Task Model                         │    │
│  │  - User ownership filtering                        │    │
│  │  - CRUD operations                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Neon PostgreSQL Database                       │
│  - tasks table (id, title, description, completed,          │
│                 user_id, created_at, updated_at)            │
│  - users table (from Feature 002)                           │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
Dashboard Page (/tasks)
│
├─ Authentication Guard
│  └─ Redirect to /auth/signin if not authenticated
│
├─ Page State Management
│  ├─ tasks: Task[]
│  ├─ loading: boolean
│  ├─ error: string
│  ├─ isCreating: boolean
│  └─ editingTaskId: number | null
│
├─ TaskForm Component (Create Mode)
│  ├─ Props: onSubmit, loading
│  └─ State: title, description, validation errors
│
├─ TaskList Component
│  ├─ Props: tasks, onToggle, onEdit, onDelete
│  └─ Renders: TaskCard[] or EmptyState
│
└─ TaskCard Component (per task)
   ├─ Props: task, onToggle, onEdit, onDelete, isEditing
   ├─ Display Mode: Show task details
   └─ Edit Mode: Inline TaskForm
```

## Key Architectural Decisions

### Decision 1: Single-Page Dashboard vs. Separate Routes

**Chosen**: Single-page dashboard with inline create/edit

**Rationale**:
- Simpler implementation with fewer files
- Better UX - no page navigation for common operations
- Faster development - single state management context
- Consistent with modern SPA patterns

**Alternatives Considered**:
- Separate `/tasks/new` and `/tasks/[id]/edit` routes
  - Rejected: Adds unnecessary complexity and navigation overhead
  - Would require route parameters and navigation state management
  - Slower user experience with page transitions

**Trade-offs**:
- Pro: Faster, simpler, better UX
- Con: Slightly more complex state management in single component
- Mitigation: Well-structured component hierarchy keeps code organized

### Decision 2: State Management Approach

**Chosen**: React useState + useEffect (local component state)

**Rationale**:
- Sufficient for single-page dashboard
- No external dependencies required
- Simpler to understand and maintain
- Aligns with Next.js App Router patterns

**Alternatives Considered**:
- React Query / SWR for data fetching
  - Rejected: Adds dependency and complexity for minimal benefit
  - Caching not critical for task dashboard (real-time updates preferred)
  - Would require learning curve for team
- Redux / Zustand for global state
  - Rejected: Overkill for single-page feature
  - No need for cross-page state sharing

**Trade-offs**:
- Pro: Simple, no dependencies, easy to debug
- Con: Manual cache invalidation, no automatic refetching
- Mitigation: Explicit refresh after mutations keeps UI in sync

### Decision 3: Component Structure

**Chosen**: Functional components with hooks, composition over inheritance

**Rationale**:
- Modern React best practices
- Hooks provide clean state and lifecycle management
- Composition allows flexible component reuse
- Consistent with existing codebase patterns

**Component Hierarchy**:
```
TasksPage (Smart Component)
├─ TaskForm (Controlled Component)
├─ TaskList (Presentational Component)
│  └─ TaskCard (Presentational Component)
│     └─ TaskForm (Edit Mode)
├─ EmptyState (Presentational Component)
└─ LoadingSpinner (Presentational Component)
```

### Decision 4: Styling Approach

**Chosen**: Tailwind CSS utility classes

**Rationale**:
- Already configured in project
- Responsive utilities built-in
- Consistent with existing pages (auth pages)
- Fast development with utility-first approach

**Responsive Breakpoints**:
- Mobile: 320px - 767px (stacked layout)
- Tablet: 768px - 1023px (2-column grid)
- Desktop: 1024px+ (3-column grid)

### Decision 5: Error Handling Strategy

**Chosen**: User-friendly error messages with retry capability

**Rationale**:
- Aligns with existing error handling from Feature 002
- Provides clear feedback without exposing technical details
- Allows users to recover from transient failures

**Error Categories**:
- Authentication errors (401) → Redirect to sign-in
- Authorization errors (403) → "You don't have permission"
- Not found errors (404) → "Task not found"
- Validation errors (422) → Inline form validation
- Server errors (500) → "Something went wrong, please try again"

## Implementation Phases

### Phase 0: Foundation Setup
**Goal**: Prepare component structure and types

**Tasks**:
1. Create `frontend/components/` directory
2. Define TypeScript interfaces in `lib/types.ts`
3. Set up component file stubs
4. Verify existing API client works with task endpoints

**Deliverables**:
- Component directory structure
- TypeScript type definitions
- Empty component files ready for implementation

### Phase 1: View Tasks (User Story 1 - P1)
**Goal**: Display user's task list

**Tasks**:
1. Create `/tasks` page with authentication guard
2. Implement TaskList component
3. Implement TaskCard component (display mode)
4. Implement EmptyState component
5. Implement LoadingSpinner component
6. Fetch tasks on page load
7. Add responsive grid layout

**Deliverables**:
- Working dashboard that displays tasks
- Empty state for new users
- Loading state during fetch
- Responsive layout (mobile/desktop)

**Acceptance Criteria**:
- User sees only their tasks after sign-in
- Empty state shows when no tasks exist
- Tasks display title, description, completion status, date
- Layout adapts to screen size

### Phase 2: Create Tasks (User Story 2 - P1)
**Goal**: Add new task functionality

**Tasks**:
1. Implement TaskForm component (create mode)
2. Add form validation (title required)
3. Integrate POST /tasks endpoint
4. Add task to list on successful creation
5. Handle creation errors
6. Clear form after successful creation

**Deliverables**:
- Working task creation form
- Validation feedback
- Optimistic UI update
- Error handling

**Acceptance Criteria**:
- User can create task with title and optional description
- Validation prevents empty titles
- New task appears immediately in list
- Form clears after creation

### Phase 3: Toggle Completion (User Story 3 - P1)
**Goal**: Mark tasks complete/incomplete

**Tasks**:
1. Add checkbox to TaskCard
2. Integrate PUT /tasks/{id} endpoint for completion toggle
3. Update task state optimistically
4. Add visual indication for completed tasks (strikethrough)
5. Handle toggle errors with rollback
6. Add keyboard support (Space key)

**Deliverables**:
- Working completion toggle
- Visual feedback for completed tasks
- Optimistic updates with error rollback
- Keyboard accessibility

**Acceptance Criteria**:
- Checkbox toggles completion status
- Completed tasks show strikethrough
- Changes persist after page refresh
- Keyboard navigation works

### Phase 4: Edit Tasks (User Story 4 - P2)
**Goal**: Update task details

**Tasks**:
1. Add "Edit" button to TaskCard
2. Switch TaskCard to edit mode (inline TaskForm)
3. Integrate PUT /tasks/{id} endpoint
4. Update task in list on successful edit
5. Add "Cancel" button to discard changes
6. Handle edit errors

**Deliverables**:
- Inline task editing
- Save/cancel functionality
- Validation feedback
- Error handling

**Acceptance Criteria**:
- User can edit task title and description
- Changes save on submit
- Cancel discards changes
- Validation prevents empty titles

### Phase 5: Delete Tasks (User Story 5 - P2)
**Goal**: Remove tasks

**Tasks**:
1. Add "Delete" button to TaskCard
2. Implement confirmation dialog
3. Integrate DELETE /tasks/{id} endpoint
4. Remove task from list on successful deletion
5. Handle deletion errors

**Deliverables**:
- Working task deletion
- Confirmation dialog
- Optimistic UI update
- Error handling

**Acceptance Criteria**:
- User can delete tasks with confirmation
- Task removed from list immediately
- Deletion persists after page refresh
- Cancel preserves task

### Phase 6: Polish & Accessibility
**Goal**: Responsive design and accessibility

**Tasks**:
1. Refine responsive layouts for all screen sizes
2. Add keyboard navigation for all interactions
3. Ensure WCAG 2.1 Level AA compliance
4. Add focus indicators
5. Test with screen readers
6. Optimize performance for 100+ tasks

**Deliverables**:
- Fully responsive dashboard
- Complete keyboard navigation
- WCAG 2.1 Level AA compliance
- Performance optimizations

**Acceptance Criteria**:
- Works on mobile (320px+) and desktop (1024px+)
- All functions accessible via keyboard
- Screen reader compatible
- Handles 100+ tasks smoothly

## Testing Strategy

### Manual Testing Approach

**Test Scenarios** (from spec.md acceptance criteria):

1. **Authentication Guard**
   - Verify unauthenticated users redirect to sign-in
   - Verify authenticated users see dashboard

2. **Task Display**
   - Create 5 tasks via API, verify all appear
   - Verify empty state with no tasks
   - Verify task details display correctly

3. **Task Creation**
   - Create task with title only
   - Create task with title and description
   - Attempt to create task without title (validation)
   - Verify new task appears in list

4. **Completion Toggle**
   - Toggle incomplete task to complete
   - Toggle complete task to incomplete
   - Verify visual indication (strikethrough)
   - Refresh page, verify status persists

5. **Task Editing**
   - Edit task title
   - Edit task description
   - Cancel edit (verify no changes)
   - Attempt to save empty title (validation)

6. **Task Deletion**
   - Delete task with confirmation
   - Cancel deletion (verify task remains)
   - Refresh page, verify deletion persists

7. **Responsive Design**
   - Test on mobile device (320px - 767px)
   - Test on tablet (768px - 1023px)
   - Test on desktop (1024px+)
   - Verify layout adapts appropriately

8. **Keyboard Navigation**
   - Tab through all interactive elements
   - Use Space to toggle completion
   - Use Enter to submit forms
   - Verify focus indicators visible

9. **Error Handling**
   - Simulate API failures (network disconnect)
   - Verify error messages display
   - Verify retry capability

10. **Multi-User Isolation**
    - Sign in as User A, create tasks
    - Sign in as User B, verify only User B's tasks visible

### Performance Testing

**Metrics to Validate**:
- Page load time < 2 seconds (measure with DevTools)
- Task operation response < 1 second (measure with DevTools)
- Smooth scrolling with 100+ tasks (visual inspection)
- No memory leaks during extended use (DevTools Memory profiler)

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API endpoint changes | High | Low | Use existing endpoints from Feature 002, no changes needed |
| Authentication token expiration during use | Medium | Medium | Existing error handling redirects to sign-in |
| State synchronization issues | Medium | Low | Explicit refresh after mutations, optimistic updates with rollback |
| Performance with many tasks | Low | Low | React virtualization if needed (not in initial scope) |
| Browser compatibility | Low | Low | Target modern browsers, use standard React/Next.js patterns |

### Implementation Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep (adding features) | Medium | Medium | Strict adherence to spec, defer enhancements to future iterations |
| Inconsistent UI patterns | Low | Low | Follow existing auth page patterns, use Tailwind consistently |
| Accessibility gaps | Medium | Low | Manual testing with keyboard and screen reader |
| Mobile layout issues | Low | Low | Mobile-first development, test on real devices |

## Dependencies

### Internal Dependencies

**Feature 002: Authentication and Multi-User Task Isolation** (BLOCKING)
- Status: ✅ Complete
- Required: JWT authentication, task API endpoints, user isolation
- Impact: Cannot start without working authentication and API

### External Dependencies

**Next.js 16+ and React 18+**
- Status: ✅ Already installed
- Required: App Router, Server Components, Client Components
- Impact: Core framework for frontend

**Tailwind CSS**
- Status: ✅ Already configured
- Required: Responsive utilities, styling
- Impact: UI styling and responsive design

**Better Auth**
- Status: ✅ Already integrated
- Required: Authentication state, session management
- Impact: Authentication guard and user context

**FastAPI Backend**
- Status: ✅ Already running
- Required: Task CRUD endpoints
- Impact: All data operations

## Success Criteria

### Technical Success Criteria

- [ ] All 5 user stories implemented and tested
- [ ] Dashboard loads in < 2 seconds
- [ ] Task operations complete in < 1 second
- [ ] Responsive design works on mobile (320px+) and desktop (1024px+)
- [ ] Keyboard navigation functional for all operations
- [ ] Error handling provides clear user feedback
- [ ] No console errors or warnings
- [ ] Code follows existing project conventions

### User Experience Success Criteria

- [ ] Users can view all their tasks immediately after sign-in
- [ ] Task creation is intuitive and fast
- [ ] Completion toggle provides immediate visual feedback
- [ ] Edit and delete operations are discoverable and safe (confirmation)
- [ ] Empty state guides new users
- [ ] Error messages are helpful and actionable
- [ ] Mobile experience is smooth and usable

### Quality Criteria

- [ ] Constitution compliance verified (all gates passed)
- [ ] No new dependencies introduced
- [ ] Consistent with existing codebase patterns
- [ ] Manual testing completed for all scenarios
- [ ] Documentation updated (quickstart.md)

## Next Steps

1. **Phase 0**: Create research.md with technical decisions documented
2. **Phase 1**: Create data-model.md, contracts/, and quickstart.md
3. **Phase 2**: Run `/sp.tasks` to generate implementation task breakdown
4. **Implementation**: Execute tasks in priority order (P1 first)
5. **Testing**: Manual testing following test scenarios
6. **Review**: Verify all success criteria met

---

**Plan Status**: ✅ Complete and ready for Phase 0 research
**Constitution Compliance**: ✅ All gates passed
**Next Command**: Continue with Phase 0 research generation
