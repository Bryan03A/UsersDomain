const express = require('express');
const cors = require('cors');
const { Client } = require('pg');
const mongoose = require('mongoose');
const moment = require('moment');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 5020;

// CORS configuration  🚀
app.use(cors({
    origin: 'http://3.227.120.143:8080',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
}));

// PostgreSQL EC2 connection
const pgClient = new Client({
    host: process.env.PG_HOST,
    port: process.env.PG_PORT,
    database: process.env.PG_DATABASE,
    user: process.env.PG_USER,
    password: process.env.PG_PASSWORD,
});

pgClient.connect()
    .then(() => console.log('✅ Connected to PostgreSQL'))
    .catch(err => {
        console.error('❌ Error connecting to PostgreSQL:', err);
        process.exit(1);
    });

// MongoDB EC2 connection
mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => {
        console.error('❌ Error connecting to MongoDB:', err);
        process.exit(1);
    });

// Session model
const sessionSchema = new mongoose.Schema({
    userId: String,
    createdAt: Date,
    updatedAt: Date,
});
const Session = mongoose.model('Session', sessionSchema);

// Route to get the user's last connection
app.get('/last-connection', async (req, res) => {
    const { username } = req.query;

    if (!username) {
        return res.status(400).json({ error: 'Username must be provided.' });
    }

    try {
        const result = await pgClient.query('SELECT id FROM "user" WHERE username = $1', [username]);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'User not found.' });
        }

        const userId = result.rows[0].id;

        const lastSession = await Session.findOne({ userId }).sort({ createdAt: -1 });

        if (!lastSession) {
            return res.status(404).json({ error: 'No sessions found for this user.' });
        }

        const timeAgo = moment(lastSession.createdAt).fromNow();

        return res.json({
            userId,
            lastConnection: timeAgo,
        });

    } catch (error) {
        console.error('Error:', error);
        return res.status(500).json({ error: 'An internal server error occurred.' });
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`✅ Session Service running on port ${port}`);
});