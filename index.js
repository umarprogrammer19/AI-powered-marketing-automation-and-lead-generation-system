const express = require('express');
const cors = require('cors');
// const cron = require('node-cron');
const { initDb, saveLead } = require('./src/db');
const { analyzeText } = require('./src/ai');
const { runRedditScraper, runFacebookScraper, runTwitterScraper } = require('./src/apify');

const app = express();
app.use(cors());
app.use(express.json());

initDb();

const DOMAIN_KEYWORDS = ["domain", ".com", "selling", "buying", "brand name", "startup name", ".pk", ".in", ".co"];

const isDomainRelated = (text) => {
    if (!text) return false;
    return DOMAIN_KEYWORDS.some(k => text.toLowerCase().includes(k));
};

// --- DATA NORMALIZER (Updated for Twitter) ---
const normalizeItem = (item, platform) => {
    let data = {};

    if (platform === 'facebook') {
        data = {
            content: item.text || "",
            url: item.url,
            subreddit: item.groupTitle || "Facebook Group",
            author_name: item.user ? item.user.name : "Unknown",
            author_id: item.user ? item.user.id : null,
            platform: 'facebook'
        };
    } else if (platform === 'reddit') {
        data = {
            content: `${item.title || ''}\n${item.body || ''}`.trim(),
            url: item.url,
            subreddit: item.communityName || "Unknown Subreddit",
            author_name: item.username || "Unknown",
            author_id: item.userId || null,
            platform: 'reddit'
        };
    } else if (platform === 'twitter') {
        const author = item.author || item.user || {};
        const username = author.userName || author.screen_name || "unknown";
        const tweetId = item.id || item.id_str;

        data = {
            content: item.text || item.full_text || "",
            url: `https://twitter.com/${username}/status/${tweetId}`,
            subreddit: "Twitter Search", 
            author_name: author.name || username,
            author_id: username, 
            platform: 'twitter'
        };
    }
    return data;
};

// --- CORE PROCESSOR (Updated) ---
const processLeads = async (platform) => {
    let items = [];
    if (platform === 'reddit') items = await runRedditScraper();
    if (platform === 'facebook') items = await runFacebookScraper();
    if (platform === 'twitter') items = await runTwitterScraper();

    console.log(`🔎 Scanned ${items.length} items from ${platform}`);
    let savedCount = 0;

    for (const item of items) {
        const leadData = normalizeItem(item, platform);

        if (!leadData.content || leadData.content.length < 5) continue;
        if (!isDomainRelated(leadData.content)) continue;

        const aiResult = await analyzeText(leadData.content, platform);

        if (["buyer", "seller", "founder"].includes(aiResult.intent) && aiResult.score !== "low") {
            await saveLead({ ...leadData, ai: aiResult });
            savedCount++;
            console.log(`✅ Saved Lead: ${leadData.author_name} (${aiResult.intent})`);
        }
    }
    return { scanned: items.length, saved: savedCount };
};

// --- ROUTES ---

app.post('/run/reddit', async (req, res) => {
    const result = await processLeads('reddit');
    res.json({ status: "success", ...result });
});

app.post('/run/facebook', async (req, res) => {
    const result = await processLeads('facebook');
    res.json({ status: "success", ...result });
});

app.post('/run/twitter', async (req, res) => {
    const result = await processLeads('twitter');
    res.json({ status: "success", ...result });
});

app.get('/leads', async (req, res) => {
    const { pool } = require('./src/db');
    const result = await pool.query('SELECT * FROM leads ORDER BY created_at DESC');
    res.json(result.rows);
});

// Scheduler (Optional: Add twitter to your cron job if you want)
// cron.schedule('0 */6 * * *', async () => {
//     console.log("⏰ Running Scheduled Scrape...");
//     await processLeads('reddit');
//     await processLeads('facebook');
//     await processLeads('twitter');
// });

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
    console.log(`✅ Server running on http://localhost:${PORT}`);
});