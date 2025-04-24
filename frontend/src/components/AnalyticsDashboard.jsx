import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const AnalyticsDashboard = () => {
  const [analyticsData, setAnalyticsData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [analyticsResponse, summaryResponse] = await Promise.all([
          fetch('http://localhost:8000/analytics?days=30'),
          fetch('http://localhost:8000/analytics/summary')
        ]);

        if (!analyticsResponse.ok || !summaryResponse.ok) {
          throw new Error('Failed to fetch data');
        }

        const analytics = await analyticsResponse.json();
        const summaryData = await summaryResponse.json();

        if (analytics.error) {
          throw new Error(analytics.error);
        }

        if (summaryData.error) {
          throw new Error(summaryData.error);
        }

        setAnalyticsData(analytics.data || []);
        setSummary(summaryData.summary || {});
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-red-600">Error: {error}</div>
      </div>
    );
  }

  if (!analyticsData.length || !summary) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">No data available</div>
      </div>
    );
  }

  const chartData = {
    labels: analyticsData.map(item => item.date),
    datasets: [
      {
        label: 'Page Views',
        data: analyticsData.map(item => item.page_views),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      },
      {
        label: 'Unique Visitors',
        data: analyticsData.map(item => item.unique_visitors),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Website Analytics'
      }
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Analytics Dashboard</h1>
      
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold">Average Page Views</h3>
            <p className="text-2xl">{Math.round(summary.average_page_views || 0)}</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold">Average Unique Visitors</h3>
            <p className="text-2xl">{Math.round(summary.average_unique_visitors || 0)}</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold">Average Session Duration</h3>
            <p className="text-2xl">{(summary.average_session_duration || 0).toFixed(1)} min</p>
          </div>
        </div>
      )}

      <div className="bg-white p-4 rounded shadow">
        <Line data={chartData} options={options} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">Bounce Rate</h3>
          <p className="text-2xl">{((summary.average_bounce_rate || 0) * 100).toFixed(1)}%</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">Conversion Rate</h3>
          <p className="text-2xl">{((summary.average_conversion_rate || 0) * 100).toFixed(1)}%</p>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard; 