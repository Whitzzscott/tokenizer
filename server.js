const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/tokenize', async (req, res) => {
    const text = req.body.text;

    if (!text) {
        return res.status(400).json({ error: 'No text provided' });
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/tokenize', { text });
        res.json(response.data);
    } catch (error) {
        console.error('Error communicating with Flask:', error);
        res.status(500).json({ error: 'Failed to process the request' });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`Node.js server is running at http://localhost:${port}`);
});
