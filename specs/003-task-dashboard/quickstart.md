# Quickstart Guide: Task Dashboard Development

**Feature**: 003-task-dashboard
**Date**: 2026-02-08
**Status**: Complete

## Overview

This guide helps developers set up their environment and start implementing the responsive task dashboard feature. Follow these steps to get started quickly.

## Prerequisites

Before starting, ensure you have:

- ✅ **Feature 002 Complete**: Authentication and Multi-User Task Isolation must be fully implemented and working
- ✅ **Node.js 18+**: Check with `node --version`
- ✅ **npm**: Check with `npm --version`
- ✅ **Python 3.11+**: Check with `python --version`
- ✅ **Git**: Check with `git --version`
- ✅ **Code Editor**: VS Code recommended with TypeScript and Tailwind CSS extensions

## Environment Setup

### 1. Verify Existing Infrastructure

Ensure Feature 002 is working:

```bash
# Backend should be running
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Frontend should be running
curl http://localhost:3000
# Expected: HTML response

# Test authentication
# Sign in via UI at http://localhost:3000/auth/signin
# Verify you can access http://localhost:3000/tasks (will be 404 until we build it)
```

### 2. Check Out Feature Branch

```bash
# Ensure you're on the correct branch
git branch --show-current
# Expected: 003-task-dashboard

# If not, check out the branch
git checkout 003-task-dashboard

# Pull latest changes
git pull origin 003-task-dashboard
```

### 3. Install Dependencies

```bash
# Frontend dependencies (if any new ones added)
cd frontend
npm install

# Backend dependencies (no changes expected)
cd ../backend
pip install -r requirements.txt
```

### 4. Start Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start FastAPI server
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Verify**:
- Backend: http://localhost:8000/docs (API documentation)
- Frontend: http://localhost:3000 (Next.js app)

## Project Structure

### Files You'll Create

```
frontend/
├── app/
│   └── tasks/
│       └── page.tsx           # NEW - Main dashboard page
├── components/                # NEW - Component directory
│   ├── TaskList.tsx          # NEW
│   ├── TaskCard.tsx          # NEW
│   ├── TaskForm.tsx          # NEW
│   ├── EmptyState.tsx        # NEW
│   └── LoadingSpinner.tsx    # NEW
└── lib/
    └── types.ts              # MODIFY - Add component prop types
```

### Files You'll Modify

```
frontend/lib/types.ts          # Add TaskCardProps, TaskFormProps, etc.
```

### Files You Won't Touch

```
backend/                       # No backend changes
frontend/lib/api-client.ts    # Already has authenticatedFetch
frontend/lib/auth-client.ts   # Already configured
frontend/app/auth/            # Existing auth pages
```

## Development Workflow

### Step 1: Create Component Directory

```bash
cd frontend
mkdir -p components
```

### Step 2: Update TypeScript Types

Edit `frontend/lib/types.ts` and add component prop interfaces:

```typescript
// Add to existing types.ts

export interface TaskCardProps {
  task: Task
  onToggle: (id: number) => Promise<void>
  onEdit: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
  isEditing: boolean
  onEditModeChange: (editing: boolean) => void
}

export interface TaskFormProps {
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>
  initialData?: Partial<Task>
  loading: boolean
  onCancel?: () => void
  mode: 'create' | 'edit'
}

// ... (see data-model.md for complete interfaces)
```

### Step 3: Create Components (Bottom-Up)

**Order of Implementation** (recommended):

1. **LoadingSpinner** (simplest, no dependencies)
2. **EmptyState** (simple, no dependencies)
3. **TaskForm** (moderate complexity, form handling)
4. **TaskCard** (uses TaskForm in edit mode)
5. **TaskList** (uses TaskCard and EmptyState)
6. **TasksPage** (orchestrates everything)

### Step 4: Test Each Component

After creating each component:

1. **Visual Test**: View in browser
2. **Interaction Test**: Click buttons, fill forms
3. **Error Test**: Simulate API failures
4. **Responsive Test**: Resize browser window
5. **Keyboard Test**: Navigate with Tab, Enter, Space

### Step 5: Commit Frequently

```bash
# After each component
git add .
git commit -m "feat: add TaskForm component"

# After each user story
git commit -m "feat: implement task creation (User Story 2)"
```

## Implementation Phases

### Phase 0: Foundation (30 minutes)

**Goal**: Set up structure and types

```bash
# Create component directory
mkdir -p frontend/components

# Create empty component files
touch frontend/components/LoadingSpinner.tsx
touch frontend/components/EmptyState.tsx
touch frontend/components/TaskForm.tsx
touch frontend/components/TaskCard.tsx
touch frontend/components/TaskList.tsx

# Create dashboard page
mkdir -p frontend/app/tasks
touch frontend/app/tasks/page.tsx
```

**Deliverable**: Empty files ready for implementation

---

### Phase 1: View Tasks (2-3 hours)

**Goal**: Display user's task list

**Implementation Order**:
1. LoadingSpinner component
2. EmptyState component
3. TaskCard component (display mode only)
4. TaskList component
5. TasksPage with authentication guard and task fetching

**Test**:
- Sign in
- Verify tasks load (create some via API if needed)
- Verify empty state shows when no tasks
- Verify responsive layout

**Commit**: `feat: implement task viewing (User Story 1)`

---

### Phase 2: Create Tasks (1-2 hours)

**Goal**: Add task creation functionality

**Implementation Order**:
1. TaskForm component (create mode)
2. Add TaskForm to TasksPage
3. Integrate POST /tasks endpoint
4. Handle form submission and state update

**Test**:
- Create task with title only
- Create task with title and description
- Verify validation (empty title)
- Verify new task appears in list

**Commit**: `feat: implement task creation (User Story 2)`

---

### Phase 3: Toggle Completion (1 hour)

**Goal**: Mark tasks complete/incomplete

**Implementation Order**:
1. Add checkbox to TaskCard
2. Integrate PUT /tasks/{id} endpoint
3. Implement optimistic update
4. Add visual indication (strikethrough)

**Test**:
- Toggle task completion
- Verify visual feedback
- Verify persistence (refresh page)
- Test error handling (disconnect network)

**Commit**: `feat: implement completion toggle (User Story 3)`

---

### Phase 4: Edit Tasks (1-2 hours)

**Goal**: Update task details

**Implementation Order**:
1. Add "Edit" button to TaskCard
2. Implement edit mode (show TaskForm inline)
3. Integrate PUT /tasks/{id} endpoint
4. Handle save/cancel

**Test**:
- Edit task title
- Edit task description
- Cancel edit (verify no changes)
- Verify validation

**Commit**: `feat: implement task editing (User Story 4)`

---

### Phase 5: Delete Tasks (1 hour)

**Goal**: Remove tasks

**Implementation Order**:
1. Add "Delete" button to TaskCard
2. Implement confirmation dialog
3. Integrate DELETE /tasks/{id} endpoint
4. Handle deletion and state update

**Test**:
- Delete task with confirmation
- Cancel deletion
- Verify task removed from list
- Verify persistence

**Commit**: `feat: implement task deletion (User Story 5)`

---

### Phase 6: Polish (2-3 hours)

**Goal**: Responsive design and accessibility

**Tasks**:
1. Refine responsive layouts
2. Add keyboard navigation
3. Test accessibility
4. Optimize performance

**Test**:
- Test on mobile device
- Test keyboard navigation
- Test with screen reader
- Test with 100+ tasks

**Commit**: `feat: add responsive design and accessibility`

---

## Common Development Tasks

### Run Frontend Dev Server

```bash
cd frontend
npm run dev
```

### Run Backend Dev Server

```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn src.main:app --reload --port 8000
```

### Check TypeScript Errors

```bash
cd frontend
npx tsc --noEmit
```

### Format Code

```bash
cd frontend
npx prettier --write "**/*.{ts,tsx}"
```

### View API Documentation

Open http://localhost:8000/docs in browser

### Test API Endpoints

```bash
# Get JWT token from browser DevTools (Application > Cookies)
TOKEN="your-token-here"

# Test GET /tasks
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/tasks
```

## Debugging Tips

### Frontend Debugging

**React DevTools**:
1. Install React DevTools browser extension
2. Open DevTools → Components tab
3. Inspect component props and state

**Network Debugging**:
1. Open DevTools → Network tab
2. Filter by "Fetch/XHR"
3. Inspect request/response for API calls

**Console Logging**:
```typescript
console.log("Tasks loaded:", tasks)
console.log("Form data:", { title, description })
```

### Backend Debugging

**FastAPI Logs**:
- Check terminal running uvicorn
- Look for request logs and errors

**API Testing**:
- Use http://localhost:8000/docs for interactive testing
- Test endpoints with different payloads

### Common Issues

**Issue**: "Authorization header missing"
- **Solution**: Ensure you're signed in and JWT token is valid

**Issue**: "CORS error"
- **Solution**: Verify backend CORS allows http://localhost:3000

**Issue**: "Task not found (404)"
- **Solution**: Verify task ID exists and belongs to current user

**Issue**: "Component not rendering"
- **Solution**: Check console for errors, verify imports

## Testing Checklist

Before marking a phase complete, verify:

### Functionality
- [ ] Feature works as specified
- [ ] All acceptance criteria met
- [ ] Error handling works
- [ ] Loading states display

### UI/UX
- [ ] Responsive on mobile and desktop
- [ ] Visual feedback for actions
- [ ] Error messages clear
- [ ] Loading indicators present

### Code Quality
- [ ] No TypeScript errors
- [ ] No console errors
- [ ] Code follows existing patterns
- [ ] Components properly typed

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] ARIA labels present
- [ ] Color contrast sufficient

## Resources

### Documentation
- [Next.js 16 Docs](https://nextjs.org/docs)
- [React 18 Docs](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Project Documentation
- `specs/003-task-dashboard/spec.md` - Feature specification
- `specs/003-task-dashboard/plan.md` - Architectural plan
- `specs/003-task-dashboard/data-model.md` - Data structures
- `specs/003-task-dashboard/contracts/` - Component and API contracts

### Existing Code References
- `frontend/app/auth/signin/page.tsx` - Example auth page
- `frontend/lib/api-client.ts` - API client wrapper
- `frontend/lib/types.ts` - Existing type definitions

## Getting Help

### Stuck on Implementation?
1. Review component contracts in `contracts/components.md`
2. Check data model in `data-model.md`
3. Review existing auth pages for patterns
4. Check API contracts in `contracts/api-integration.md`

### API Issues?
1. Test endpoint with curl or Postman
2. Check backend logs for errors
3. Verify JWT token is valid
4. Review API documentation at http://localhost:8000/docs

### UI Issues?
1. Check browser console for errors
2. Inspect element with DevTools
3. Review Tailwind CSS documentation
4. Test in different browsers

## Next Steps

After completing implementation:

1. **Manual Testing**: Follow test scenarios in `plan.md`
2. **Code Review**: Review your own code for quality
3. **Documentation**: Update any relevant docs
4. **Commit**: Make final commit with summary
5. **Demo**: Test the complete user flow
6. **Merge**: Create pull request to main branch

---

**Quickstart Status**: ✅ Complete
**Ready for Implementation**: Yes
**Estimated Time**: 8-12 hours total
