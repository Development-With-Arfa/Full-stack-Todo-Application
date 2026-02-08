import { Pool } from 'pg';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '.env.local') });

async function createJwksTable() {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('Connecting to database...');
    const client = await pool.connect();

    console.log('Creating jwks table...');
    await client.query(`
      CREATE TABLE IF NOT EXISTS jwks (
        id VARCHAR(255) PRIMARY KEY,
        "publicKey" TEXT NOT NULL,
        "privateKey" TEXT NOT NULL,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
      );
    `);

    console.log('✓ jwks table created successfully!');
    client.release();
  } catch (error) {
    console.error('✗ Failed to create jwks table:', error.message);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

createJwksTable();
