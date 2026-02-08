import { Pool } from 'pg';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env.local
dotenv.config({ path: join(__dirname, '.env.local') });

async function runMigration() {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('Connecting to database...');
    const client = await pool.connect();

    console.log('Reading SQL schema...');
    const sql = readFileSync(join(__dirname, 'better-auth-schema.sql'), 'utf-8');

    console.log('Executing migration...');
    await client.query(sql);

    console.log('✓ Migration completed successfully!');
    console.log('✓ Better Auth tables created:');
    console.log('  - user');
    console.log('  - session');
    console.log('  - account');
    console.log('  - verification');

    client.release();
  } catch (error) {
    console.error('✗ Migration failed:', error.message);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

runMigration();
