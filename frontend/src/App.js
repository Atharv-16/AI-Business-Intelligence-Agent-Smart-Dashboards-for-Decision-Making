import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Container, Grid } from '@mui/material';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import ChatInterface from './components/ChatInterface';
import { LanguageProvider } from './contexts/LanguageContext';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LanguageProvider>
        <Container maxWidth="xl" sx={{ py: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <AnalyticsDashboard />
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ height: '80vh' }}>
                <ChatInterface />
              </Box>
            </Grid>
          </Grid>
        </Container>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App; 