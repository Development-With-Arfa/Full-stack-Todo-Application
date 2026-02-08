# Todo App with Authentication

A secure, multi-user task management application built with Next.js, FastAPI, and PostgreSQL. Features JWT-based authentication with Better Auth and complete task isolation between users.

## Features

- ✅ User registration and authentication
- ✅ JWT-based session management (24-hour tokens)
- ✅ Secure multi-user task isolation
- ✅ Complete CRUD operations for tasks
- ✅ Real-time task updates
- ✅ Responsive UI with Tailwind CSS
- ✅ Type-safe API with TypeScript and Pydantic
- ✅ Database migrations with Alembic

## Tech Stack

### Frontend
- **Next.js 16+** - React framework with App Router
- **TypeScript** - Type safety
- **Better Auth** - Authentication with JWT plugin
- **Tailwind CSS** - Styling
- **HTTP-only cookies** - Secure session storage

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **PostgreSQL** - Database (Neon)
- **Alembic** - Database migrations
- **PyJWT** - JWT verification with JWKS
- **Pydantic** - Data validation

## Security Features

- **Asymmetric JWT Verification**: Backend verifies tokens using JWKS endpoint (no shared secrets)
- **HTTP-only Cookies**: Session tokens not accessible to JavaScript
- **User Ownership Enforcement**: All task operations verify user ownership
- **Input Validation**: Pydantic schemas validate all API inputs
- **CORS Protection**: Configured for specific frontend origin
- **Error Message Safety**: Generic errors that don't leak sensitive information

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (Neon recommended)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Todo_App_II
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scriptsctivate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/database
JWKS_URL=http://localhost:3000/api/auth/jwks
ISSUER=http://localhost:3000
AUDIENCE=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

Edit `frontend/.env.local`:
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=<generate-with-openssl-rand-base64-32>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Generate `BETTER_AUTH_SECRET`:
```bash
openssl rand -base64 32
```

### 4. Database Setup

```bash
cd backend

# Run migrations
alembic upgrade head
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
venv\Scriptsctivate  # Windows
uvicorn src.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:3000

## Usage

### 1. Register a New Account

1. Navigate to http://localhost:3000/auth/signup
2. Enter email and password (min 8 chars, must include letter and number)
3. Click "Sign Up"
4. Automatically redirected to tasks page

### 2. Sign In

1. Navigate to http://localhost:3000/auth/signin
2. Enter your credentials
3. Click "Sign In"
4. Redirected to tasks page

### 3. Manage Tasks

- **Create Task**: Fill in title (required) and description (optional), click "Add Task"
- **Complete Task**: Click checkbox to toggle completion status
- **Delete Task**: Click "Delete" button (with confirmation)
- **Sign Out**: Click "Sign Out" button in top-right

## API Documentation

### Authentication

All task endpoints require JWT Bearer token in Authorization header.

### Endpoints

#### Get All Tasks
- **GET** `/api/v1/tasks`
- **Auth**: Required
- **Response**: 200 OK with array of tasks

#### Create Task
- **POST** `/api/v1/tasks`
- **Auth**: Required
- **Body**: `{"title": "string", "description": "string"}`
- **Response**: 201 Created

#### Update Task
- **PUT** `/api/v1/tasks/{task_id}`
- **Auth**: Required
- **Body**: `{"title": "string", "completed": boolean}`
- **Response**: 200 OK

#### Delete Task
- **DELETE** `/api/v1/tasks/{task_id}`
- **Auth**: Required
- **Response**: 204 No Content

### Error Responses

- **401 Unauthorized**: Authentication required or invalid token
- **403 Forbidden**: User doesn't own the resource
- **404 Not Found**: Resource not found
- **422 Validation Error**: Invalid input data

## Testing

See testing guides:
- `backend/tests/test_multi_user_security.md` - Multi-user isolation tests
- `backend/tests/test_token_expiration.md` - Token expiration tests

## Troubleshooting

### "Authentication token is invalid"
- Token may be expired (24-hour limit)
- Sign out and sign in again
- Check that JWKS_URL is accessible from backend

### "Database connection failed"
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Ensure database exists

### "CORS error"
- Verify FRONTEND_URL in backend .env matches frontend URL
- Check CORS middleware configuration in src/main.py

## Production Deployment

### Security Checklist

- [ ] HTTPS enabled on all services
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] CORS restricted to production domain
- [ ] Rate limiting implemented
- [ ] Logging and monitoring configured

## Future Enhancements

- [ ] Refresh token implementation
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Task sharing between users
- [ ] Task categories and tags
- [ ] Automated testing suite

## License

MIT
