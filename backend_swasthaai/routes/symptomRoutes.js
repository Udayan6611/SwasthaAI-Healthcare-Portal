const express = require('express');
const router = express.Router();
const { analyzeSymptoms, handleChat } = require('../controllers/symptomController');

router.post('/analyze', analyzeSymptoms);
router.post('/chat', handleChat);

module.exports = router;