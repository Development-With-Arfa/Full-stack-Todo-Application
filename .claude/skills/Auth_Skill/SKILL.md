---
name: auth-skill
description: Secure authentication workflows (signup/signin), password hashing, JWT tokens, Better Auth integration. Use when implementing or auditing user authentication.
---

# Auth Skill — Secure Authentication

## Instructions
Implement authentication systems with these requirements:

### 1. Signup & Signin Flows
- Validate user input (email, password)
- Prevent duplicate accounts
- Return safe and minimal error messages

### 2. Password Security
- Always hash passwords using **bcrypt or argon2**
- Never store or log plain-text passwords
- Enforce strong password rules

### 3. JWT Token Handling
- Issue JWTs with correct claims (`sub`, `iat`, `exp`)
- Verify signatures on every protected request
- Reject expired or invalid tokens

### 4. Better Auth Integration
- Configure Better Auth securely
- Ensure session consistency across client/server
- Follow best practices for cookies and token transport

### 5. Security Best Practices
- Protect all sensitive endpoints with auth middleware
- Prevent token leakage and unauthorized access
- Enforce user ownership in multi-user apps

## Example Snippet (FastAPI JWT Verify)
```python
from fastapi import HTTPException
from jose import jwt, JWTError

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
