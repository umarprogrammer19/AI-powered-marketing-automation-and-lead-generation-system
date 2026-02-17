const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

const initDb = async () => {
    const query = `
    CREATE TABLE IF NOT EXISTS leads (
      id SERIAL PRIMARY KEY,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      content TEXT,
      url TEXT,
      subreddit TEXT, 
      platform TEXT,
      author_name TEXT, 
      author_id TEXT,
      intent TEXT,
      score TEXT,
      context TEXT,
      outreach TEXT,
      status TEXT DEFAULT 'new'
    );
  `;
    try {
        await pool.query(query);
        console.log("✅ Database initialized (Table 'leads' ready)");
    } catch (err) {
        console.error("❌ DB Init Error:", err);
    }
};

const saveLead = async (lead) => {
    const query = `
    INSERT INTO leads (content, url, subreddit, platform, author_name, author_id, intent, score, context, outreach, status)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 'new')
    RETURNING *;
  `;
    const values = [
        lead.content,
        lead.url,
        lead.subreddit,
        lead.platform,
        lead.author_name,
        lead.author_id,
        lead.ai.intent,
        lead.ai.score,
        lead.ai.context,
        lead.ai.outreach
    ];

    return pool.query(query, values);
};

module.exports = { pool, initDb, saveLead };