const axios = require('axios');

const PYTHON_API_URL = 'http://127.0.0.1:5001';

exports.analyzeSymptoms = async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_API_URL}/predict`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error proxying to Python /predict:', error.message);
        res.status(500).json({ error: 'AI service is not responding.' });
    }
};

exports.handleChat = async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_API_URL}/chat`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error proxying to Python /chat:', error.message);
        res.status(500).json({ error: 'Chatbot service is not responding.' });
    }
};
