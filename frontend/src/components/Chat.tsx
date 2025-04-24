import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import Plot from 'react-plotly.js';
import axios from 'axios';

interface Message {
  text: string;
  isUser: boolean;
  data?: any;
  visualization?: any;
  followUpQuestions?: string[];
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      text: input,
      isUser: true,
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/query', {
        text: input,
        language,
      });

      const botMessage: Message = {
        text: response.data.text,
        isUser: false,
        data: response.data.data,
        visualization: response.data.visualization,
        followUpQuestions: response.data.follow_up_questions,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        text: 'Sorry, there was an error processing your request.',
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const handleFollowUpClick = (question: string) => {
    setInput(question);
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', p: 2 }}>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h5" gutterBottom>
          Business Intelligence Assistant
        </Typography>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Language</InputLabel>
          <Select
            value={language}
            label="Language"
            onChange={(e) => setLanguage(e.target.value)}
          >
            <MenuItem value="en">English</MenuItem>
            <MenuItem value="zh">中文</MenuItem>
            <MenuItem value="yue">粵語</MenuItem>
          </Select>
        </FormControl>
        <Box sx={{ height: 400, overflow: 'auto', mb: 2 }}>
          <List>
            {messages.map((message, index) => (
              <ListItem
                key={index}
                sx={{
                  flexDirection: 'column',
                  alignItems: message.isUser ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 1,
                    bgcolor: message.isUser ? 'primary.light' : 'grey.100',
                    maxWidth: '80%',
                  }}
                >
                  <ListItemText
                    primary={message.text}
                    sx={{ color: message.isUser ? 'white' : 'inherit' }}
                  />
                </Paper>
                {message.visualization && (
                  <Box sx={{ width: '100%', mt: 1 }}>
                    <Plot
                      data={message.visualization.data}
                      layout={message.visualization.layout}
                      style={{ width: '100%' }}
                    />
                  </Box>
                )}
                {message.followUpQuestions && (
                  <Box sx={{ mt: 1, width: '100%' }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Follow-up questions:
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      {message.followUpQuestions.map((question, qIndex) => (
                        <Button
                          key={qIndex}
                          size="small"
                          variant="outlined"
                          onClick={() => handleFollowUpClick(question)}
                        >
                          {question}
                        </Button>
                      ))}
                    </Box>
                  </Box>
                )}
              </ListItem>
            ))}
          </List>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            disabled={loading}
          />
          <Button
            variant="contained"
            endIcon={<SendIcon />}
            onClick={handleSend}
            disabled={loading}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Chat; 