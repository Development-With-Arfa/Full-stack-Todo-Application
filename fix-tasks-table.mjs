import { Pool } from 'pg';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '../frontend/.env.local') });

async function fixTasksTable() {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('Connecting to database...');
    const client = await pool.connect();

    console.log('Dropping existing tasks table...');
    await client.query('DROP TABLE IF EXISTS tasks CASCADE;');

    console.log('Creating tasks table with correct schema...');
    await client.query(`
      CREATE TABLE tasks (
        id UUID PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(1000),
        completed BOOLEAN NOT NULL DEFAULT FALSE,
        user_id VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      );
    `);

    console.log('Creating index on user_id...');
    await client.query('CREATE INDEX idx_tasks_user_id ON tasks(user_id);');

    console.log('✓ Tasks table fixed successfully!');
    client.release();
  } catch (error) {
    console.error('✗ Failed to fix tasks table:', error.message);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

fixTasksTable();
