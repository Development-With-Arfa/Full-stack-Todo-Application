# Research: Responsive Task Dashboard

**Feature**: 003-task-dashboard
**Date**: 2026-02-08
**Status**: Complete

## Overview

This document consolidates technical research and architectural decisions for the responsive task dashboard feature. Since this feature builds entirely on existing infrastructure (Feature 002), most technical decisions are straightforward extensions of established patterns.

## Technical Decisions

### Decision 1: Component Architecture Pattern

**Question**: What component architecture pattern should we use for the dashboard?

**Research Findings**:
- Next.js 16+ App Router supports both Server and Client Components
- Task dashboard requires interactivity (state, event handlers) → Client Components
- Existing auth pages use Client Components with "use client" directive
- React 18+ hooks (useState, useEffect) are standard for state management

**Decision**: Use Client Components with React hooks

**Rationale**:
- Consistent with existing codebase patterns
- Hooks provide clean state and lifecycle management
- No server-side rendering needed for authenticated dashboard
- Simpler than mixing Server and Client Components

**Implementation**:
```typescript
"use client"

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  // ... rest of component
}
```

---

### Decision 2: State Management Strategy

**Question**: Should we use local state, context, or external state management?

**Research Findings**:
- Dashboard is single-page application
- No state sharing needed across routes
- React Query/SWR adds 50KB+ bundle size
- useState + useEffect sufficient for CRUD operations
- Existing auth pages use local state successfully

**Decision**: Local component state with useState + useEffect

**Rationale**:
- Zero additional dependencies
- Sufficient for single-page dashboard
- Easy to understand and maintain
- Explicit control over data fetching and updates

**Trade-offs**:
- Pro: Simple, no dependencies, predictable
- Con: Manual cache invalidation
- Mitigation: Explicit refresh after mutations

**Implementation Pattern**:
```typescript
// Fetch on mount
useEffect(() => {
  loadTasks()
}, [])

// Refresh after mutations
const handleCreateTask = async (data) => {
  await createTask(data)
  await loadTasks() // Explicit refresh
}
```

---

### Decision 3: Form Handling Approach

**Question**: Should we use a form library (React Hook Form, Formik) or controlled components?

**Research Findings**:
- Task form has only 2 fields (title, description)
- Validation is simple (title required, max lengths)
- React Hook Form adds 40KB bundle size
- Existing auth forms use controlled components
- Controlled components sufficient for simple forms

**Decision**: Controlled components with manual validation

**Rationale**:
- No additional dependencies
- Simple validation logic (title required)
- Consistent with existing auth forms
- Adequate for 2-field form

**Implementation**:
```typescript
const [title, setTitle] = useState("")
const [description, setDescription] = useState("")
const [errors, setErrors] = useState<{title?: string}>({})

const validate = () => {
  if (!title.trim()) {
    setErrors({ title: "Title is required" })
    return false
  }
  return true
}
```

---

### Decision 4: Responsive Layout Strategy

**Question**: How should we implement responsive design?

**Research Findings**:
- Tailwind CSS already configured in project
- Tailwind provides responsive utilities (sm:, md:, lg:, xl:)
- Mobile-first approach is Tailwind best practice
- Existing auth pages use Tailwind responsive classes

**Decision**: Tailwind CSS responsive utilities with mobile-first approach

**Rationale**:
- Already available, no setup needed
- Mobile-first aligns with spec requirements
- Consistent with existing pages
- Fast development with utility classes

**Breakpoint Strategy**:
```typescript
// Mobile (default): Stacked layout
<div className="space-y-4">

// Tablet (md:): 2-column grid
<div className="space-y-4 md:grid md:grid-cols-2 md:gap-4">

// Desktop (lg:): 3-column grid
<div className="space-y-4 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-4">
```

---

### Decision 5: API Integration Pattern

**Question**: How should components interact with the backend API?

**Research Findings**:
- Existing `lib/api-client.ts` provides `authenticatedFetch` wrapper
- Automatically attaches JWT Bearer tokens
- Handles 401/403 errors
- Used successfully in existing features

**Decision**: Use existing `authenticatedFetch` wrapper

**Rationale**:
- Already implemented and tested
- Automatic JWT token attachment
- Consistent error handling
- No new code needed

**Usage Pattern**:
```typescript
import { authenticatedFetch } from "@/lib/api-client"

const loadTasks = async () => {
  const response = await authenticatedFetch("/api/v1/tasks")
  const data = await response.json()
  setTasks(data)
}
```

---

### Decision 6: Error Handling Strategy

**Question**: How should we handle and display errors?

**Research Findings**:
- Existing auth pages show inline error messages
- Backend returns structured error responses
- User-friendly messages defined in backend (Feature 002)
- Toast notifications not in scope

**Decision**: Inline error messages with retry capability

**Rationale**:
- Consistent with existing error handling
- Simple to implement
- Clear user feedback
- No additional dependencies

**Implementation**:
```typescript
const [error, setError] = useState("")

try {
  await operation()
} catch (err: any) {
  setError(err.message || "Operation failed")
}

// Display
{error && (
  <div className="bg-red-50 p-4 rounded">
    <p className="text-red-800">{error}</p>
  </div>
)}
```

---

### Decision 7: Accessibility Implementation

**Question**: How do we ensure WCAG 2.1 Level AA compliance?

**Research Findings**:
- Keyboard navigation required for all interactions
- Focus indicators must be visible
- Color contrast must meet 4.5:1 ratio
- Screen reader compatibility needed
- Tailwind provides focus utilities

**Decision**: Semantic HTML + Tailwind focus utilities + ARIA labels

**Rationale**:
- Semantic HTML provides baseline accessibility
- Tailwind focus utilities (focus:ring, focus:outline) handle visual indicators
- ARIA labels for screen readers
- No additional libraries needed

**Implementation Checklist**:
- [ ] Use semantic HTML (button, form, input)
- [ ] Add focus:ring-2 focus:ring-blue-500 to interactive elements
- [ ] Provide aria-label for icon buttons
- [ ] Ensure color contrast meets 4.5:1
- [ ] Test with keyboard navigation
- [ ] Test with screen reader

---

### Decision 8: Component File Organization

**Question**: Where should components be located?

**Research Findings**:
- Next.js 16+ App Router supports colocation
- Can place components in `app/` or separate `components/` directory
- Existing project has no `components/` directory yet
- Auth pages are self-contained in `app/auth/`

**Decision**: Create `frontend/components/` directory for reusable components

**Rationale**:
- Separates reusable components from page-specific code
- Cleaner organization as project grows
- Standard Next.js pattern
- Easy to import: `@/components/TaskCard`

**Structure**:
```
frontend/
├── app/
│   └── tasks/
│       └── page.tsx          # Page-specific logic
└── components/               # Reusable components
    ├── TaskList.tsx
    ├── TaskCard.tsx
    ├── TaskForm.tsx
    ├── EmptyState.tsx
    └── LoadingSpinner.tsx
```

---

### Decision 9: TypeScript Type Definitions

**Question**: Where should TypeScript types be defined?

**Research Findings**:
- Existing `lib/types.ts` has Task interface (from Feature 002)
- Types should be centralized for reuse
- Component prop types can be inline or exported

**Decision**: Extend `lib/types.ts` with component prop interfaces

**Rationale**:
- Centralized type definitions
- Easy to import across components
- Consistent with existing pattern
- Type safety across codebase

**Types to Add**:
```typescript
// Task types (already exist)
export interface Task { ... }

// Component prop types (new)
export interface TaskCardProps {
  task: Task
  onToggle: (id: number) => void
  onEdit: (id: number) => void
  onDelete: (id: number) => void
  isEditing: boolean
}

export interface TaskFormProps {
  onSubmit: (data: TaskCreate) => void
  initialData?: Partial<Task>
  loading: boolean
}
```

---

### Decision 10: Loading State Implementation

**Question**: How should we indicate loading states?

**Research Findings**:
- Loading states needed for: initial load, create, edit, delete, toggle
- Existing auth pages use simple loading text
- Spinner component provides better UX
- Tailwind has animation utilities

**Decision**: LoadingSpinner component + disabled states

**Rationale**:
- Better UX than text-only loading
- Prevents duplicate submissions
- Consistent loading indicator
- Simple to implement with Tailwind

**Implementation**:
```typescript
// LoadingSpinner component
export function LoadingSpinner() {
  return (
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
  )
}

// Usage in forms
<button disabled={loading}>
  {loading ? <LoadingSpinner /> : "Save"}
</button>
```

---

## Technology Stack Summary

### Frontend Stack (Confirmed)
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.x
- **UI Library**: React 18+
- **Styling**: Tailwind CSS 3.x
- **Authentication**: Better Auth (existing)
- **HTTP Client**: Fetch API with authenticatedFetch wrapper

### Backend Stack (Existing, No Changes)
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: JWT with JWKS verification

### Development Tools
- **Package Manager**: npm
- **Linting**: ESLint (existing config)
- **Type Checking**: TypeScript compiler
- **Testing**: Manual testing (automated tests not in scope)

---

## Best Practices Applied

### React Best Practices
1. **Functional Components**: Use hooks instead of class components
2. **Composition**: Build complex UIs from simple components
3. **Single Responsibility**: Each component has one clear purpose
4. **Controlled Components**: Forms use controlled inputs
5. **Key Props**: Unique keys for list items (task.id)

### Next.js Best Practices
1. **Client Components**: Use "use client" for interactive components
2. **File-based Routing**: Leverage App Router conventions
3. **TypeScript**: Full type safety across codebase
4. **Import Aliases**: Use @/ for clean imports

### Accessibility Best Practices
1. **Semantic HTML**: Use appropriate HTML elements
2. **Keyboard Navigation**: All interactions keyboard-accessible
3. **Focus Management**: Visible focus indicators
4. **ARIA Labels**: Screen reader support
5. **Color Contrast**: Meet WCAG 2.1 Level AA standards

### Performance Best Practices
1. **Optimistic Updates**: Update UI before API response
2. **Error Rollback**: Revert on failure
3. **Minimal Re-renders**: Proper state management
4. **Code Splitting**: Automatic with Next.js

---

## Open Questions

**None** - All technical decisions are clear and documented above.

---

## References

- [Next.js 16 Documentation](https://nextjs.org/docs)
- [React 18 Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- Feature 002 Implementation (existing codebase)

---

**Research Status**: ✅ Complete
**All Decisions Documented**: Yes
**Ready for Phase 1**: Yes
