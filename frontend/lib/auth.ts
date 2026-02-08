import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"
import { Kysely, PostgresDialect } from "kysely"
import { Pool } from "pg"

// Create PostgreSQL connection pool with SSL for Neon
const pool = new Pool({
  connectionString: process.env.DATABASE_URL!,
  ssl: {
    rejectUnauthorized: false
  }
})

// Create Kysely instance with PostgreSQL dialect
const db = new Kysely({
  dialect: new PostgresDialect({
    pool: pool
  })
})

export const auth = betterAuth({
  database: {
    provider: "postgres",
    db: db,
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      jwt: {
        expirationTime: "24h",
        issuer: process.env.BETTER_AUTH_URL!,
        audience: process.env.BETTER_AUTH_URL!,
      }
    })
  ],
})
