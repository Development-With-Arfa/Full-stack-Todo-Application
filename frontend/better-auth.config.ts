export default {
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!,
  },
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
}
