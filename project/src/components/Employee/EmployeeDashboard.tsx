import React, { useState, useEffect } from 'react';
import { MessageSquare, Calendar, Check, Clock } from 'lucide-react';
import { api } from '../../utils/api';
import { Feedback } from '../../types';

const EmployeeDashboard: React.FC = () => {
  const [feedback, setFeedback] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeedback();
  }, []);

  const fetchFeedback = async () => {
    try {
      const data = await api.getFeedback();
      setFeedback(data);
    } catch (error) {
      console.error('Error fetching feedback:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (feedbackId: number) => {
    try {
      await api.acknowledgeFeedback(feedbackId);
      fetchFeedback();
    } catch (error) {
      console.error('Error acknowledging feedback:', error);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-50 border-green-200';
      case 'negative': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😔';
      default: return '😐';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Feedback</h1>
        <p className="mt-2 text-gray-600">View and acknowledge feedback from your manager</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <MessageSquare className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Feedback</p>
              <p className="text-3xl font-bold text-gray-900">{feedback.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Check className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Acknowledged</p>
              <p className="text-3xl font-bold text-gray-900">
                {feedback.filter(f => f.acknowledged_at).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-amber-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-3xl font-bold text-gray-900">
                {feedback.filter(f => !f.acknowledged_at).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Timeline */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Feedback Timeline</h2>
        
        {feedback.length === 0 ? (
          <div className="text-center py-12">
            <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No feedback received yet</p>
          </div>
        ) : (
          <div className="space-y-6">
            {feedback.map((item) => (
              <div key={item.id} className="relative">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className={`w-4 h-4 rounded-full ${
                      item.acknowledged_at ? 'bg-green-500' : 'bg-gray-300'
                    }`} />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className={`p-6 rounded-lg border-2 ${getSentimentColor(item.sentiment)}`}>
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <span className="text-lg">
                            {getSentimentIcon(item.sentiment)}
                          </span>
                          <span className="font-medium text-gray-900">
                            Feedback from {item.manager_name}
                          </span>
                          <span className="text-sm text-gray-500">
                            {new Date(item.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        {!item.acknowledged_at && (
                          <button
                            onClick={() => handleAcknowledge(item.id)}
                            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors text-sm"
                          >
                            Acknowledge
                          </button>
                        )}
                      </div>
                      
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-medium text-gray-900 mb-2">Strengths</h4>
                          <p className="text-gray-700">{item.strengths}</p>
                        </div>
                        
                        <div>
                          <h4 className="font-medium text-gray-900 mb-2">Areas to Improve</h4>
                          <p className="text-gray-700">{item.areas_to_improve}</p>
                        </div>
                      </div>
                      
                      {item.acknowledged_at && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <p className="text-sm text-gray-500">
                            Acknowledged on {new Date(item.acknowledged_at).toLocaleDateString()}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmployeeDashboard;