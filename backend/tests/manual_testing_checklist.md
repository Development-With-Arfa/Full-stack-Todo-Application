# Manual Testing Checklist

Complete guide for T055 (edge cases) and T057 (acceptance scenarios).

## T055: Edge Case Testing

### Test 1: Malformed JWT Tokens
- [ ] Remove characters from token middle
- [ ] Add random characters to token
- [ ] Verify 401 Unauthorized response
- [ ] Verify error message is user-friendly

### Test 2: Concurrent Sign-Ins
- [ ] Sign in from Chrome and Firefox simultaneously
- [ ] Verify both sessions work independently
- [ ] Create tasks in both browsers
- [ ] Verify task synchronization

### Test 3: Rapid Failed Attempts
- [ ] Attempt 10 failed sign-ins rapidly
- [ ] Verify consistent error messages
- [ ] Verify system remains responsive
- [ ] Verify successful sign-in works after failures

### Test 4: Missing Authorization Header
- [ ] Make API request without auth header
- [ ] Verify 401 Unauthorized
- [ ] Verify no data returned

### Test 5: Expired Token
- [ ] Wait 24+ hours or modify token expiration
- [ ] Attempt API request with expired token
- [ ] Verify 401 and redirect to sign-in

### Test 6: Token Tampering
- [ ] Modify token payload (user ID)
- [ ] Attempt to use modified token
- [ ] Verify signature verification fails

### Test 7: Concurrent Operations
- [ ] Open two tabs, same user
- [ ] Create tasks simultaneously
- [ ] Verify no race conditions

## T057: Acceptance Scenarios

### User Story 1: Registration

**Scenario 1.1: Successful Registration**
- [ ] Navigate to /auth/signup
- [ ] Enter valid email and password
- [ ] Verify account created
- [ ] Verify redirect to /tasks

**Scenario 1.2: Duplicate Email**
- [ ] Register existing email
- [ ] Verify error message
- [ ] Verify no duplicate created

**Scenario 1.3: Weak Password**
- [ ] Try password without numbers
- [ ] Try password without letters
- [ ] Try password under 8 chars
- [ ] Verify validation errors

**Scenario 1.4: Invalid Email**
- [ ] Try invalid email format
- [ ] Verify validation error

### User Story 2: Sign In

**Scenario 2.1: Successful Sign In**
- [ ] Sign in with valid credentials
- [ ] Verify redirect to /tasks
- [ ] Verify session persists

**Scenario 2.2: Invalid Credentials**
- [ ] Try wrong password
- [ ] Try non-existent email
- [ ] Verify generic error message

**Scenario 2.3: Session Persistence**
- [ ] Refresh page after sign in
- [ ] Close and reopen browser
- [ ] Verify session maintained

### User Story 3: Task Isolation

**Scenario 3.1: Own Tasks Only**
- [ ] Create tasks as User A
- [ ] Sign in as User B
- [ ] Verify User B sees only their tasks

**Scenario 3.2: Cannot Access Others Tasks**
- [ ] Get User A task ID
- [ ] Sign in as User B
- [ ] Try GET/PUT/DELETE on User A task
- [ ] Verify 403 Forbidden

**Scenario 3.3: Auth Required**
- [ ] Sign out
- [ ] Try to access /tasks
- [ ] Verify redirect to sign-in

**Scenario 3.4: Auto User Association**
- [ ] Create task (no user_id input)
- [ ] Verify task.user_id set correctly

### User Story 4: Sign Out

**Scenario 4.1: Successful Sign Out**
- [ ] Click Sign Out button
- [ ] Verify redirect to sign-in
- [ ] Verify session invalidated

**Scenario 4.2: Token Invalid After Sign Out**
- [ ] Capture token before sign out
- [ ] Sign out
- [ ] Try to use old token
- [ ] Verify 401 Unauthorized

**Scenario 4.3: Back Button Protection**
- [ ] Sign out
- [ ] Click browser back button
- [ ] Verify redirect to sign-in

## Testing Tools

- Browser DevTools (Network, Application tabs)
- Postman or curl for API testing
- jwt.io for token inspection
- Database client for verification

## Sign-Off

Tester: _______________
Date: _______________
All Tests Passed: [ ] Yes [ ] No
