# Token Expiration Testing Guide

## Overview
This document outlines test cases for JWT token expiration and refresh behavior.

## Configuration
- Token expiration time: 24 hours (configured in frontend/lib/auth.ts)
- Issuer: http://localhost:3000
- Audience: http://localhost:8000

## Test Cases

### TC-001: Valid Token Acceptance
**Objective:** Verify that valid, non-expired tokens are accepted

**Steps:**
1. Sign in as a user
2. Immediately make API request with fresh token
3. Verify 200 OK response

**Expected Result:**
- Request succeeds
- User can access protected resources
- No authentication errors

**Status:** [ ] Pass [ ] Fail

---

### TC-002: Expired Token Rejection
**Objective:** Verify that expired tokens are rejected

**Steps:**
1. Sign in as a user
2. Manually set token expiration to past time (or wait 24 hours)
3. Attempt to access /api/v1/tasks
4. Verify 401 Unauthorized response

**Expected Result:**
- API returns 401 Unauthorized
- Error message: "Your session has expired. Please sign in again."
- User redirected to sign-in page

**Status:** [ ] Pass [ ] Fail

---

### TC-003: Token Expiration Near Boundary
**Objective:** Verify behavior when token is about to expire

**Steps:**
1. Sign in as a user
2. Wait until token is 1 minute from expiration
3. Make API request
4. Verify request succeeds

**Expected Result:**
- Request succeeds while token is still valid
- No premature rejection
- Token expiration enforced at exact expiry time

**Status:** [ ] Pass [ ] Fail

---

### TC-004: Frontend Token Refresh
**Objective:** Verify that frontend handles token expiration gracefully

**Steps:**
1. Sign in as a user
2. Simulate token expiration
3. Attempt to create a task
4. Verify user is redirected to sign-in page
5. Sign in again
6. Verify user can resume work

**Expected Result:**
- User sees clear error message
- Automatic redirect to sign-in after 2 seconds
- After re-authentication, user can continue working
- No data loss

**Status:** [ ] Pass [ ] Fail

---

### TC-005: Multiple Expired Token Requests
**Objective:** Verify consistent behavior for multiple requests with expired token

**Steps:**
1. Sign in as a user
2. Let token expire
3. Make multiple API requests (GET, POST, PUT, DELETE)
4. Verify all return 401 Unauthorized

**Expected Result:**
- All requests consistently return 401
- Error messages are consistent
- No partial operations succeed

**Status:** [ ] Pass [ ] Fail

---

### TC-006: Token Expiration During Long Session
**Objective:** Verify behavior when token expires during active session

**Steps:**
1. Sign in as a user
2. Keep browser open for 24+ hours
3. Attempt to create a task
4. Verify appropriate error handling

**Expected Result:**
- User sees session expired message
- Redirected to sign-in page
- Can sign in again without issues

**Status:** [ ] Pass [ ] Fail

---

### TC-007: Sign Out Invalidates Token
**Objective:** Verify that signing out prevents further token use

**Steps:**
1. Sign in as a user, capture token
2. Sign out
3. Attempt to use captured token for API request
4. Verify 401 Unauthorized response

**Expected Result:**
- Token no longer valid after sign out
- API returns 401 Unauthorized
- User must sign in again

**Status:** [ ] Pass [ ] Fail

---

### TC-008: Token Validation Error Messages
**Objective:** Verify that token validation errors are user-friendly

**Steps:**
1. Test various invalid token scenarios:
   - Malformed token
   - Expired token
   - Invalid signature
   - Missing token
2. Verify error messages don't leak sensitive information

**Expected Result:**
- Error messages are generic and user-friendly
- No stack traces or internal details exposed
- Consistent error format across all scenarios

**Status:** [ ] Pass [ ] Fail

---

## Testing Tools

### Manual Testing
1. Browser DevTools (Network tab to inspect tokens)
2. JWT.io to decode and inspect token payload
3. Postman/Insomnia to test API directly

### Automated Testing
```python
# Example pytest test for token expiration
import pytest
from datetime import datetime, timedelta
import jwt

def test_expired_token_rejected(client, test_user):
    # Create expired token
    expired_token = create_token(
        user_id=test_user.id,
        exp=datetime.utcnow() - timedelta(hours=1)
    )
    
    # Attempt to access protected endpoint
    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()
```

## Token Expiration Configuration

### Current Settings
- **Expiration Time:** 24 hours
- **Algorithm:** EdDSA (Ed25519)
- **Issuer:** http://localhost:3000
- **Audience:** http://localhost:8000

### Recommended Production Settings
- **Expiration Time:** 1-2 hours (shorter for better security)
- **Refresh Token:** Implement refresh token mechanism
- **Algorithm:** EdDSA (Ed25519) - keep current
- **Issuer:** https://yourdomain.com
- **Audience:** https://api.yourdomain.com

## Security Considerations

- [ ] Token expiration time is appropriate for use case
- [ ] Expired tokens are consistently rejected
- [ ] No token reuse after sign out
- [ ] Error messages don't leak sensitive information
- [ ] Token validation uses JWKS endpoint (asymmetric verification)
- [ ] No tokens stored in localStorage (using HTTP-only cookies)
- [ ] Token refresh mechanism planned for production

## Future Enhancements

1. **Refresh Token Implementation**
   - Long-lived refresh tokens (7-30 days)
   - Automatic token refresh before expiration
   - Refresh token rotation for security

2. **Token Revocation**
   - Maintain revocation list for compromised tokens
   - Immediate invalidation on security events

3. **Activity-Based Expiration**
   - Extend token on user activity
   - Shorter expiration for inactive sessions
