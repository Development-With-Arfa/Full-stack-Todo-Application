# Todo Full-Stack Multi-User Web Application Constitution

## Core Principles

### Secure Multi-User Task Isolation and Ownership Enforcement
All task operations must be authenticated and filtered by the authenticated user ID; no user may access, modify, or view tasks belonging to another user; strict access control and validation required at every task endpoint.

### Reliable Backend Persistence with Neon PostgreSQL
All task data must be persisted to Neon Serverless PostgreSQL using SQLModel ORM; data integrity and consistency must be maintained through ACID transactions; proper error handling for database operations required.

### Clear Separation of Frontend, Backend, and Authentication Layers
Frontend (Next.js 16+) must communicate with backend (Python FastAPI) through well-defined RESTful API endpoints; authentication layer (Better Auth) must be separate from business logic; proper decoupling and interface contracts maintained.

### Production-Grade REST API Design and Validation
All task operations must follow RESTful principles with consistent JSON response formats; proper HTTP status codes must be returned for all endpoints; request/response validation and sanitization required.

### Consistent JWT Authentication and Authorization
Every API request must be authenticated using JWT Bearer tokens; backend must verify JWT signatures using shared Better Auth secret; authentication middleware must be applied consistently across all protected endpoints.

### Responsive and Accessible Frontend UI
All task workflows must be implemented with responsive design principles; accessibility standards (WCAG) must be followed; consistent UI/UX patterns applied across all user interactions.

## Technology Stack Constraints
Frontend: Next.js 16+ (App Router) | Backend: Python FastAPI | ORM: SQLModel | Database: Neon Serverless PostgreSQL | Authentication: Better Auth with JWT plugin enabled

All technology choices must adhere to the specified stack; no additional frameworks or libraries may be introduced without explicit architectural approval; third-party dependencies must be vetted for security and maintainability.

## Development Standards
RESTful API design with proper HTTP methods and status codes; JWT authentication for all task endpoints; database queries filtered by authenticated user ID; consistent JSON response formats; proper error handling and validation at all layers; comprehensive testing coverage for all critical paths.

## Governance

All code must comply with this constitution; any deviation requires explicit architectural approval documented in an ADR; all pull requests must be reviewed for constitutional compliance; security and authentication requirements are non-negotiable.

**Version**: 1.0.0 | **Ratified**: 2026-02-04 | **Last Amended**: 2026-02-04
