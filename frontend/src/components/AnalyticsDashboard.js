import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { 
  Card, 
  CardContent, 
  Typography, 
  Grid, 
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box
} from '@mui/material';
import { useLanguage } from '../contexts/LanguageContext';
import { languages } from '../config/languages';

const AnalyticsDashboard = () => {
  const { t, currentLanguage, changeLanguage } = useLanguage();
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        const response = await fetch('http://localhost:8000/analytics?days=30');
        const data = await response.json();
        setAnalyticsData(data.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch analytics data');
        setLoading(false);
      }
    };

    fetchAnalyticsData();
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!analyticsData) return null;

  // Calculate summary metrics
  const totalUsers = analyticsData.reduce((sum, day) => sum + day.users, 0);
  const avgBounceRate = analyticsData.reduce((sum, day) => sum + day.bounce_rate, 0) / analyticsData.length;
  const totalRevenue = analyticsData.reduce((sum, day) => sum + day.revenue, 0);

  return (
    <div style={{ padding: '20px' }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          {t('dashboard.title')}
        </Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Language</InputLabel>
          <Select
            value={currentLanguage}
            label="Language"
            onChange={(e) => changeLanguage(e.target.value)}
          >
            {Object.values(languages).map((lang) => (
              <MenuItem key={lang.code} value={lang.code}>
                {lang.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} style={{ marginBottom: '20px' }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary">{t('dashboard.totalUsers')}</Typography>
              <Typography variant="h4">{totalUsers.toLocaleString()}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary">{t('dashboard.avgBounceRate')}</Typography>
              <Typography variant="h4">{(avgBounceRate * 100).toFixed(1)}%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary">{t('dashboard.totalRevenue')}</Typography>
              <Typography variant="h4">${totalRevenue.toLocaleString()}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>{t('dashboard.usersOverTime')}</Typography>
              <Plot
                data={[
                  {
                    x: analyticsData.map(d => d.date),
                    y: analyticsData.map(d => d.users),
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: t('dashboard.dailyUsers')
                  }
                ]}
                layout={{
                  width: '100%',
                  height: 300,
                  title: t('dashboard.dailyUsers')
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>{t('dashboard.revenueOverTime')}</Typography>
              <Plot
                data={[
                  {
                    x: analyticsData.map(d => d.date),
                    y: analyticsData.map(d => d.revenue),
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: t('dashboard.dailyRevenue')
                  }
                ]}
                layout={{
                  width: '100%',
                  height: 300,
                  title: t('dashboard.dailyRevenue')
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>{t('dashboard.bounceRateTrend')}</Typography>
              <Plot
                data={[
                  {
                    x: analyticsData.map(d => d.date),
                    y: analyticsData.map(d => d.bounce_rate * 100),
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: t('dashboard.dailyBounceRate')
                  }
                ]}
                layout={{
                  width: '100%',
                  height: 300,
                  title: t('dashboard.dailyBounceRate')
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>{t('dashboard.sessionDuration')}</Typography>
              <Plot
                data={[
                  {
                    x: analyticsData.map(d => d.date),
                    y: analyticsData.map(d => d.avg_session_duration),
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: t('dashboard.avgSessionDuration')
                  }
                ]}
                layout={{
                  width: '100%',
                  height: 300,
                  title: t('dashboard.avgSessionDuration')
                }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default AnalyticsDashboard; 