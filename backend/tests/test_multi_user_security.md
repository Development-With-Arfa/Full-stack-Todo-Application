# Multi-User Security Testing Guide

## Overview
This document outlines the test cases for verifying multi-user task isolation and security in the Todo App.

## Test Environment Setup

### Prerequisites
1. Backend server running on http://localhost:8000
2. Frontend server running on http://localhost:3000
3. PostgreSQL database with clean state
4. Two test user accounts:
   - User A: usera@example.com / password123
   - User B: userb@example.com / password123

## Test Cases

### TC-001: User Registration Isolation
**Objective:** Verify that users can register independently without conflicts

**Steps:**
1. Register User A with usera@example.com
2. Register User B with userb@example.com
3. Verify both users can sign in independently

**Expected Result:**
- Both users created successfully
- Each user has unique ID in database
- No cross-contamination of user data

**Status:** [ ] Pass [ ] Fail

---

### TC-002: Task Creation Isolation
**Objective:** Verify that tasks are automatically associated with the correct user

**Steps:**
1. Sign in as User A
2. Create Task A1: "User A's first task"
3. Create Task A2: "User A's second task"
4. Sign out
5. Sign in as User B
6. Create Task B1: "User B's first task"
7. Verify User B only sees Task B1

**Expected Result:**
- User A sees only Task A1 and A2
- User B sees only Task B1
- Database shows correct user_id for each task

**Status:** [ ] Pass [ ] Fail

---

### TC-003: Task Read Authorization
**Objective:** Verify users cannot read other users' tasks

**Steps:**
1. Sign in as User A, create Task A1, note its ID
2. Sign out, sign in as User B
3. Attempt to GET /api/v1/tasks/{Task A1 ID} using User B's token
4. Verify 403 Forbidden response

**Expected Result:**
- API returns 403 Forbidden
- Error message: "You don't have permission to access this task."
- User B cannot see Task A1 details

**Status:** [ ] Pass [ ] Fail

---

### TC-004: Task Update Authorization
**Objective:** Verify users cannot update other users' tasks

**Steps:**
1. Sign in as User A, create Task A1, note its ID
2. Sign out, sign in as User B
3. Attempt to PUT /api/v1/tasks/{Task A1 ID} with User B's token
4. Verify 403 Forbidden response

**Expected Result:**
- API returns 403 Forbidden
- Error message: "You don't have permission to access this task."
- Task A1 remains unchanged in database

**Status:** [ ] Pass [ ] Fail

---

### TC-005: Task Delete Authorization
**Objective:** Verify users cannot delete other users' tasks

**Steps:**
1. Sign in as User A, create Task A1, note its ID
2. Sign out, sign in as User B
3. Attempt to DELETE /api/v1/tasks/{Task A1 ID} with User B's token
4. Verify 403 Forbidden response

**Expected Result:**
- API returns 403 Forbidden
- Error message: "You don't have permission to access this task."
- Task A1 still exists in database

**Status:** [ ] Pass [ ] Fail

---

### TC-006: Task List Isolation
**Objective:** Verify GET /tasks only returns current user's tasks

**Steps:**
1. Sign in as User A, create 3 tasks
2. Sign out, sign in as User B, create 2 tasks
3. Verify User B's GET /tasks returns exactly 2 tasks
4. Sign out, sign in as User A
5. Verify User A's GET /tasks returns exactly 3 tasks

**Expected Result:**
- Each user sees only their own tasks
- Task counts match expected values
- No cross-user task visibility

**Status:** [ ] Pass [ ] Fail

---

### TC-007: Token Tampering Protection
**Objective:** Verify that modified JWT tokens are rejected

**Steps:**
1. Sign in as User A, capture JWT token
2. Modify the token payload (change user ID)
3. Attempt to access /api/v1/tasks with modified token
4. Verify 401 Unauthorized response

**Expected Result:**
- API returns 401 Unauthorized
- Error message: "Authentication token is invalid. Please sign in again."
- No access granted with tampered token

**Status:** [ ] Pass [ ] Fail

---

### TC-008: Missing Token Protection
**Objective:** Verify that requests without tokens are rejected

**Steps:**
1. Attempt to GET /api/v1/tasks without Authorization header
2. Verify 401 Unauthorized response

**Expected Result:**
- API returns 401 Unauthorized
- Error message indicates authentication required
- No task data returned

**Status:** [ ] Pass [ ] Fail

---

### TC-009: Concurrent User Operations
**Objective:** Verify that concurrent operations by different users don't interfere

**Steps:**
1. Open two browser windows
2. Sign in as User A in window 1
3. Sign in as User B in window 2
4. Simultaneously create tasks in both windows
5. Verify each user sees only their own tasks

**Expected Result:**
- Both users can operate independently
- No race conditions or data corruption
- Task isolation maintained under concurrent load

**Status:** [ ] Pass [ ] Fail

---

### TC-010: Session Persistence
**Objective:** Verify that user sessions persist across page refreshes

**Steps:**
1. Sign in as User A
2. Create a task
3. Refresh the page
4. Verify user is still signed in and sees their tasks

**Expected Result:**
- User remains authenticated after refresh
- Tasks are still visible
- No re-authentication required

**Status:** [ ] Pass [ ] Fail

---

## Manual Testing Checklist

- [ ] All test cases executed
- [ ] All test cases passed
- [ ] No security vulnerabilities found
- [ ] Error messages are user-friendly and don't leak sensitive info
- [ ] Database queries verified to include user_id filters
- [ ] JWT tokens verified using JWKS endpoint
- [ ] CORS configuration allows only frontend origin

## Automated Testing Notes

These test cases should be automated using:
- Backend: pytest with FastAPI TestClient
- Frontend: Jest/Vitest with React Testing Library
- E2E: Playwright or Cypress

## Security Audit Checklist

- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection via SameSite cookies
- [ ] JWT signature verification working
- [ ] No sensitive data in JWT payload
- [ ] HTTPS enforced in production
- [ ] Rate limiting implemented (future)
- [ ] Input validation on all endpoints
