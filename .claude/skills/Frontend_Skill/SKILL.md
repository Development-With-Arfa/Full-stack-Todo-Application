---
name: frontend-skill
description: Frontend development skill for building responsive pages, reusable components, layouts, and styling. Use when working on UI with React/Next.js.
---

# Frontend Skill — Pages, Components & Styling

## Instructions
Build frontend interfaces with these requirements:

### 1. Page & Layout Development
- Create structured pages using Next.js App Router
- Use consistent layouts (dashboard, auth pages, task pages)
- Support responsive design for mobile and desktop

### 2. Component Building
- Build reusable UI components (buttons, forms, modals, cards)
- Follow modern React patterns (hooks, props, state)
- Keep components clean and maintainable

### 3. Styling & UI Consistency
- Apply styling with Tailwind CSS or UI libraries
- Maintain consistent spacing, typography, and colors
- Ensure accessible and user-friendly design

### 4. Frontend–Backend Integration
- Connect UI to REST APIs correctly (fetch/axios)
- Handle loading, success, and error states properly
- Ensure secure token/session usage when required

### 5. UX Best Practices
- Provide clear navigation and smooth interactions
- Use form validation and helpful feedback messages
- Optimize for performance and accessibility

## Example Snippet (Next.js Component)
```tsx
export default function TaskCard({ title }: { title: string }) {
  return (
    <div className="p-4 rounded-xl shadow-md bg-white">
      <h2 className="text-lg font-semibold">{title}</h2>
    </div>
  );
}
