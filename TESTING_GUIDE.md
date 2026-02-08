# Testing Guide - Feature 003: Task Dashboard

**Date**: 2026-02-08
**Status**: Ready for Manual Testing
**Servers**: Frontend (http://localhost:3001) | Backend (http://localhost:8001)

---

## ✅ Implementation Status

**Completed**: 50/63 tasks (79%)

### Phases Complete:
- ✅ Phase 1: Setup (4/4 tasks)
- ✅ Phase 2: Foundational (3/3 tasks)
- ✅ Phase 3: User Story 1 - View Tasks (9/9 tasks)
- ✅ Phase 4: User Story 2 - Create Tasks (9/9 tasks)
- ✅ Phase 5: User Story 3 - Toggle Completion (8/8 tasks)
- ✅ Phase 6: User Story 4 - Edit Tasks (10/10 tasks)
- ✅ Phase 7: User Story 5 - Delete Tasks (7/7 tasks)
- 🔄 Phase 8: Polish & Testing (10/13 tasks)

### Remaining Tasks:
- [ ] T054: Test keyboard navigation
- [ ] T055: Test with screen reader
- [ ] T061: Test multi-user isolation
- [ ] T062: Test authentication token expiration
- [ ] T063: Run manual testing checklist

---

## 🔧 Prerequisites

Before testing, verify:

1. **Backend Running**: http://localhost:8001
   ```bash
   curl http://localhost:8001/health
   # Expected: {"status":"healthy"}
   ```

2. **Frontend Running**: http://localhost:3001
   ```bash
   # Open in browser - should load
   ```

3. **Database Tables Created**: Better Auth tables exist in Neon PostgreSQL
   - ✅ user
   - ✅ session
   - ✅ account
   - ✅ verification

---

## 📋 Manual Testing Checklist

### Test 1: Authentication Flow (T061 - Multi-User Isolation)

**Objective**: Verify users can only see their own tasks

#### Steps:

1. **Create First User**
   - Navigate to http://localhost:3001/auth/signup
   - Email: `user1@test.com`
   - Password: `Password123!`
   - Click "Sign Up"
   - ✅ Should redirect to http://localhost:3001/tasks
   - ✅ Should see empty state (no tasks yet)

2. **Create Tasks for User 1**
   - Create 3 tasks:
     - "User 1 Task A"
     - "User 1 Task B"
     - "User 1 Task C"
   - ✅ All tasks should appear in the list

3. **Sign Out User 1**
   - Navigate to http://localhost:3001/auth/signin
   - Sign out (if sign out button exists) or clear cookies manually:
     - Open DevTools → Application → Cookies
     - Delete all cookies for localhost:3001

4. **Create Second User**
   - Navigate to http://localhost:3001/auth/signup
   - Email: `user2@test.com`
   - Password: `Password123!`
   - Click "Sign Up"
   - ✅ Should redirect to http://localhost:3001/tasks
   - ✅ Should see empty state (User 1's tasks should NOT be visible)

5. **Create Tasks for User 2**
   - Create 2 tasks:
     - "User 2 Task X"
     - "User 2 Task Y"
   - ✅ Only User 2's tasks should be visible
   - ✅ User 1's tasks should NOT appear

6. **Switch Back to User 1**
   - Sign out User 2 (clear cookies)
   - Sign in as `user1@test.com` / `Password123!`
   - ✅ Should only see User 1's 3 tasks
   - ✅ User 2's tasks should NOT appear

**Expected Result**: ✅ Complete task isolation between users

---

### Test 2: Keyboard Navigation (T054)

**Objective**: Verify all operations work with keyboard only

#### Steps:

1. **Navigate to Tasks Page**
   - Sign in at http://localhost:3001/auth/signin
   - Press `Tab` to navigate through form fields
   - Press `Enter` to submit

2. **Create Task with Keyboard**
   - Press `Tab` until focus reaches "Title" input
   - Type: "Keyboard Test Task"
   - Press `Tab` to "Description" input
   - Type: "Created using keyboard only"
   - Press `Tab` to "Add Task" button
   - Press `Enter` or `Space` to submit
   - ✅ Task should be created and appear in list

3. **Toggle Completion with Keyboard**
   - Press `Tab` until focus reaches task checkbox
   - ✅ Should see visible focus indicator (blue ring)
   - Press `Space` to toggle completion
   - ✅ Task should show strikethrough
   - Press `Space` again to toggle back
   - ✅ Strikethrough should be removed

4. **Edit Task with Keyboard**
   - Press `Tab` until focus reaches "Edit" button
   - Press `Enter` to activate edit mode
   - ✅ TaskForm should appear inline
   - Modify title/description using `Tab` and typing
   - Press `Tab` to "Save" button
   - Press `Enter` to save
   - ✅ Changes should be saved

5. **Delete Task with Keyboard**
   - Press `Tab` until focus reaches "Delete" button
   - Press `Enter` to trigger confirmation
   - ✅ Confirmation dialog should appear
   - Press `Enter` to confirm (or `Escape` to cancel)
   - ✅ Task should be deleted

**Expected Result**: ✅ All operations accessible via keyboard

---

### Test 3: Screen Reader Accessibility (T055)

**Objective**: Verify functionality with screen reader

**Tools**: NVDA (Windows), JAWS (Windows), or VoiceOver (macOS)

#### Steps:

1. **Enable Screen Reader**
   - Windows: Download and start NVDA (free)
   - macOS: Enable VoiceOver (Cmd+F5)

2. **Navigate to Tasks Page**
   - Sign in at http://localhost:3001/auth/signin
   - ✅ Screen reader should announce form labels
   - ✅ Should announce "Email" and "Password" fields

3. **Test Task List**
   - Navigate to tasks page
   - ✅ Should announce "Loading" state
   - ✅ Should announce number of tasks or "No tasks yet"
   - ✅ Should announce each task title and description

4. **Test Task Actions**
   - Navigate to task checkbox
   - ✅ Should announce "Mark task as complete" or similar
   - Navigate to Edit button
   - ✅ Should announce "Edit task: [title]"
   - Navigate to Delete button
   - ✅ Should announce "Delete task: [title]"

5. **Test Form**
   - Navigate to create task form
   - ✅ Should announce "Title" label and "required" status
   - ✅ Should announce "Description" label and "optional" status
   - ✅ Should announce character counts
   - ✅ Should announce validation errors

**Expected Result**: ✅ All content and actions announced clearly

---

### Test 4: Token Expiration Handling (T062)

**Objective**: Verify redirect to sign-in when token expires

#### Steps:

1. **Sign In**
   - Navigate to http://localhost:3001/auth/signin
   - Sign in with valid credentials
   - Navigate to http://localhost:3001/tasks

2. **Simulate Token Expiration**
   - Open DevTools → Application → Cookies
   - Find the Better Auth session cookie
   - Delete the session cookie
   - OR wait 24 hours (token expiration time)

3. **Attempt Task Operation**
   - Try to create a new task
   - OR try to toggle task completion
   - OR refresh the page

4. **Verify Redirect**
   - ✅ Should redirect to http://localhost:3001/auth/signin
   - ✅ Should show message like "Please sign in to continue"
   - ✅ After signing in, should return to tasks page

**Expected Result**: ✅ Graceful handling of expired tokens

---

### Test 5: Responsive Design

**Objective**: Verify layout works on all screen sizes

#### Steps:

1. **Mobile (320px - 767px)**
   - Open DevTools → Toggle device toolbar
   - Select "iPhone SE" or set width to 375px
   - ✅ Tasks should stack vertically (1 column)
   - ✅ Form should be full width
   - ✅ Buttons should be touch-friendly (min 44px)
   - ✅ Text should be readable (no horizontal scroll)

2. **Tablet (768px - 1023px)**
   - Set width to 768px
   - ✅ Tasks should display in 2 columns
   - ✅ Form should be appropriately sized
   - ✅ Layout should feel balanced

3. **Desktop (1024px+)**
   - Set width to 1280px
   - ✅ Tasks should display in 3 columns
   - ✅ Maximum width should be constrained (not too wide)
   - ✅ Spacing should be comfortable

**Expected Result**: ✅ Optimal layout at all breakpoints

---

### Test 6: Error Handling

**Objective**: Verify graceful error handling

#### Steps:

1. **Network Error Simulation**
   - Open DevTools → Network tab
   - Enable "Offline" mode
   - Try to create a task
   - ✅ Should show error message: "Failed to create task. Please try again."
   - ✅ Form should remain filled (don't lose data)
   - Disable offline mode
   - Retry submission
   - ✅ Should succeed

2. **Validation Errors**
   - Try to create task with empty title
   - ✅ Should show: "Title is required"
   - Try to create task with 300 character title
   - ✅ Should show: "Title must be 255 characters or less"
   - Try to create task with 1100 character description
   - ✅ Should show: "Description must be 1000 characters or less"

3. **Server Error Simulation**
   - Stop the backend server
   - Try to load tasks page
   - ✅ Should show error message
   - ✅ Should not crash the app

**Expected Result**: ✅ User-friendly error messages, no crashes

---

### Test 7: Performance with Many Tasks

**Objective**: Verify smooth performance with 100+ tasks

#### Steps:

1. **Create Many Tasks**
   - Use the API to bulk create tasks:
   ```bash
   # Get JWT token from browser DevTools (Application > Cookies)
   TOKEN="your-token-here"

   # Create 100 tasks
   for i in {1..100}; do
     curl -X POST http://localhost:8001/api/v1/tasks \
       -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" \
       -d "{\"title\":\"Task $i\",\"description\":\"Test task number $i\"}"
   done
   ```

2. **Test Performance**
   - Refresh the tasks page
   - ✅ Page should load within 2 seconds
   - ✅ Scrolling should be smooth (60fps)
   - ✅ No lag when toggling tasks
   - ✅ No lag when editing tasks

3. **Test Search/Filter (if implemented)**
   - ✅ Search should be responsive
   - ✅ Results should update quickly

**Expected Result**: ✅ Smooth performance with 100+ tasks

---

### Test 8: Complete User Flow

**Objective**: Test the entire user journey

#### Steps:

1. **New User Journey**
   - Navigate to http://localhost:3001
   - Click "Sign Up" (if link exists) or go to /auth/signup
   - Create account
   - ✅ Redirects to tasks page
   - ✅ Shows empty state with friendly message

2. **First Task Creation**
   - Create first task: "Buy groceries"
   - ✅ Empty state disappears
   - ✅ Task appears in list
   - ✅ Form clears after submission

3. **Task Management**
   - Create 5 more tasks
   - Toggle 2 tasks as complete
   - Edit 1 task
   - Delete 1 task
   - ✅ All operations work smoothly
   - ✅ UI updates immediately (optimistic updates)

4. **Sign Out and Back In**
   - Sign out (clear cookies)
   - Sign back in
   - ✅ All tasks still present
   - ✅ Completion states preserved

**Expected Result**: ✅ Seamless end-to-end experience

---

## 🐛 Known Issues

Document any issues found during testing:

| Issue | Severity | Steps to Reproduce | Expected | Actual |
|-------|----------|-------------------|----------|--------|
| _Example: Task not updating_ | High | 1. Edit task 2. Save | Task updates | Error shown |

---

## ✅ Sign-Off Checklist

Before marking implementation complete:

- [ ] All authentication tests pass (T061)
- [ ] Keyboard navigation works (T054)
- [ ] Screen reader accessible (T055)
- [ ] Token expiration handled (T062)
- [ ] Responsive on all screen sizes
- [ ] Error handling works correctly
- [ ] Performance acceptable with 100+ tasks
- [ ] Complete user flow works end-to-end
- [ ] No console errors
- [ ] No TypeScript errors

---

## 📝 Test Results

**Tester**: _________________
**Date**: _________________
**Overall Status**: ⬜ Pass | ⬜ Fail | ⬜ Needs Fixes

**Notes**:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________

---

## 🚀 Next Steps After Testing

1. **If all tests pass**:
   - Mark tasks T054, T055, T061, T062, T063 as complete
   - Update tasks.md with completion status
   - Commit all changes
   - Create pull request

2. **If issues found**:
   - Document issues in "Known Issues" section
   - Create fix tasks
   - Implement fixes
   - Re-test

3. **Final steps**:
   - Code review
   - Merge to main branch
   - Deploy to production
