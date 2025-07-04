export interface User {
  id: number;
  email: string;
  name: string;
  role: 'manager' | 'employee';
  manager_id?: number;
  created_at: string;
}

export interface Feedback {
  id: number;
  manager_id: number;
  employee_id: number;
  strengths: string;
  areas_to_improve: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  created_at: string;
  updated_at: string;
  acknowledged_at?: string;
  manager_name: string;
  employee_name: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

export interface FeedbackSubmission {
  employee_id: number;
  strengths: string;
  areas_to_improve: string;
  sentiment: 'positive' | 'neutral' | 'negative';
}