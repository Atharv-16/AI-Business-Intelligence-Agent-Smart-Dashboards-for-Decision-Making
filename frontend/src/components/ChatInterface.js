import React, { useState } from 'react';
import { Box, TextField, Paper, Typography, List, ListItem, Button, Chip } from '@mui/material';
import Plot from 'react-plotly.js';
import axios from 'axios';

const predefinedQuestions = {
  en: [
    "What was my bounce rate last month?",
    "How many users visited my site today?",
    "What's the average session duration?",
    "Show me the revenue trend",
    "What's the conversion rate?"
  ],
  zh: [
    "上个月的跳出率是多少？",
    "今天有多少用户访问了我的网站？",
    "平均会话时长是多少？",
    "显示收入趋势",
    "转化率是多少？"
  ],
  yue: [
    "上個月嘅跳出率係幾多？",
    "今日有幾多用戶訪問咗我嘅網站？",
    "平均會話時長係幾多？",
    "顯示收入趨勢",
    "轉化率係幾多？"
  ]
};

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('en');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await axios.post('http://localhost:8000/query', {
        text: input,
        language: language
      });

      const botMessage = {
        text: response.data.response,
        sender: 'bot',
        charts: response.data.charts || []
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error processing query:', error);
      setMessages(prev => [...prev, {
        text: 'Sorry, I encountered an error processing your query.',
        sender: 'bot'
      }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  const handlePredefinedQuestion = (question) => {
    setInput(question);
  };

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', p: 2 }}>
      <Paper elevation={3} sx={{ p: 2, height: '70vh', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <Button
            variant={language === 'en' ? 'contained' : 'outlined'}
            onClick={() => handleLanguageChange('en')}
          >
            English
          </Button>
          <Button
            variant={language === 'zh' ? 'contained' : 'outlined'}
            onClick={() => handleLanguageChange('zh')}
          >
            中文
          </Button>
          <Button
            variant={language === 'yue' ? 'contained' : 'outlined'}
            onClick={() => handleLanguageChange('yue')}
          >
            粵語
          </Button>
        </Box>

        <Box sx={{ flexGrow: 1, overflow: 'auto', mb: 2 }}>
          <List>
            {messages.map((message, index) => (
              <ListItem
                key={index}
                sx={{
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 1
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    bgcolor: message.sender === 'user' ? '#e3f2fd' : '#f5f5f5'
                  }}
                >
                  <Typography variant="body1">{message.text}</Typography>
                  {message.charts && message.charts.map((chart, idx) => (
                    <Box key={idx} sx={{ mt: 2 }}>
                      <Plot
                        data={chart.data}
                        layout={chart.layout}
                        style={{ width: '100%', height: '300px' }}
                        config={{ responsive: true }}
                      />
                    </Box>
                  ))}
                </Paper>
              </ListItem>
            ))}
          </List>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Predefined Questions
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {predefinedQuestions[language].map((question, index) => (
              <Chip
                key={index}
                label={question}
                onClick={() => handlePredefinedQuestion(question)}
                variant="outlined"
              />
            ))}
          </Box>
        </Box>

        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask about your business data..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default ChatInterface; 