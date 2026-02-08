# Deployment Guide

This guide covers deploying the Todo App to production environments.

## Deployment Options

### Recommended Stack
- **Frontend**: Vercel (Next.js optimized)
- **Backend**: Railway or Render (Python/FastAPI)
- **Database**: Neon (Serverless PostgreSQL)

## Prerequisites

- GitHub account
- Vercel account
- Railway/Render account
- Neon account
- Domain name (optional)

## Database Setup (Neon)

1. Create project at https://neon.tech
2. Copy connection strings:
   - Backend: postgresql+asyncpg://user:pass@host/db?sslmode=require
   - Frontend: postgresql://user:pass@host/db?sslmode=require
3. Run migrations: alembic upgrade head

## Backend Deployment (Railway)

1. Create Procfile: web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
2. Deploy from GitHub
3. Set environment variables:
   - DATABASE_URL
   - JWKS_URL (frontend URL + /api/auth/jwks)
   - ISSUER (frontend URL)
   - AUDIENCE (backend URL)
   - FRONTEND_URL

## Frontend Deployment (Vercel)

1. Deploy from GitHub
2. Set environment variables:
   - DATABASE_URL
   - BETTER_AUTH_SECRET (openssl rand -base64 32)
   - NEXT_PUBLIC_API_URL (backend URL)
3. Redeploy after setting variables

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] CORS configured
- [ ] Rate limiting (future)
- [ ] Monitoring enabled

## Testing Production

1. Register new account
2. Create tasks
3. Test multi-user isolation
4. Verify error handling
5. Check JWKS endpoint accessibility

## Troubleshooting

### CORS Errors
- Verify FRONTEND_URL matches exact frontend URL
- Check CORS middleware configuration

### Auth Failures
- Verify JWKS_URL is accessible
- Check ISSUER and AUDIENCE match

### Database Issues
- Verify connection string format
- Check SSL mode is included

## Cost Estimates

Free Tier: ~$5/month
- Neon: Free (0.5 GB)
- Railway: $5 credit
- Vercel: Free

Production: ~$60/month
- Neon Pro: $19
- Railway: ~$20
- Vercel Pro: $20

See README.md for detailed setup instructions.
