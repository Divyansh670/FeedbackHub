# FeedbackHub - Employee Feedback System

A comprehensive feedback management system designed for internal feedback sharing between managers and team members. Built with React frontend and Python Flask backend.

## 🌟 Features

### Core Features
- **Role-based Authentication**: Separate interfaces for managers and employees
- **Structured Feedback**: Submit feedback with strengths, areas to improve, and sentiment
- **Feedback History**: Complete timeline of feedback for both managers and employees
- **Acknowledgment System**: Employees can acknowledge received feedback
- **Dashboard Analytics**: Manager dashboard with team overview and feedback trends
- **Real-time Updates**: Instant feedback submission and acknowledgment

### User Experience
- **Clean, Modern UI**: Professional design with intuitive navigation
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Role-based Access**: Automatic routing based on user role
- **Smooth Interactions**: Hover effects and transitions for better UX

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Vite** for build tooling

### Backend
- **Python Flask** REST API
- **SQLite** database
- **JWT** authentication
- **Flask-CORS** for cross-origin requests

## 🏗️ Architecture

### Database Schema
```sql
Users Table:
- id (Primary Key)
- email (Unique)
- password_hash
- name
- role (manager/employee)
- manager_id (Foreign Key)
- created_at

Feedback Table:
- id (Primary Key)
- manager_id (Foreign Key)
- employee_id (Foreign Key)
- strengths (Text)
- areas_to_improve (Text)
- sentiment (positive/neutral/negative)
- created_at
- updated_at
- acknowledged_at
```

### API Endpoints
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user
- `GET /api/users/team` - Get team members (managers only)
- `GET /api/feedback` - Get feedback (role-based)
- `POST /api/feedback` - Submit feedback (managers only)
- `PUT /api/feedback/:id` - Update feedback (managers only)
- `POST /api/feedback/:id/acknowledge` - Acknowledge feedback (employees only)
- `GET /api/dashboard/stats` - Dashboard statistics (managers only)

## 🚀 Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- Docker (optional, for containerized deployment)

### Frontend Setup
1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

### Docker Setup (Backend)
1. Build the Docker image:
```bash
cd backend
docker build -t feedback-backend .
```

2. Run the container:
```bash
docker run -p 5000:5000 feedback-backend
```

## 👥 Demo Accounts

The system comes with pre-configured demo accounts:

**Manager Account:**
- Email: `manager@company.com`
- Password: `password123`
- Can view team members, submit feedback, and access analytics

**Employee Account:**
- Email: `employee@company.com`
- Password: `password123`
- Can view received feedback and acknowledge it

## 📱 Usage

### For Managers
1. Log in with manager credentials
2. View team overview and feedback statistics
3. Submit structured feedback for team members
4. Edit previously submitted feedback
5. Monitor team feedback trends

### For Employees
1. Log in with employee credentials
2. View timeline of received feedback
3. Acknowledge feedback to confirm receipt
4. Track feedback history and personal development

## 🔐 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing with Werkzeug
- Input validation and sanitization
- CORS configuration for secure cross-origin requests

## 🎨 Design Decisions

### User Experience
- **Role-based Routing**: Automatic redirection based on user role
- **Intuitive Interface**: Clean, modern design with consistent styling
- **Responsive Layout**: Mobile-first approach with breakpoints
- **Visual Feedback**: Loading states, hover effects, and status indicators

### Technical Decisions
- **TypeScript**: Type safety for better development experience
- **Component Architecture**: Modular, reusable components
- **State Management**: Context API for authentication state
- **API Design**: RESTful endpoints with proper HTTP status codes

### Database Design
- **Normalized Schema**: Separate tables for users and feedback
- **Foreign Key Relationships**: Proper data integrity
- **Timestamp Tracking**: Created, updated, and acknowledged timestamps
- **Role-based Access**: Database-level role checking

## 🔄 Development Workflow

1. **Authentication Flow**: JWT tokens stored in localStorage
2. **Role-based Access**: Automatic routing and component rendering
3. **Real-time Updates**: Immediate UI updates after actions
4. **Error Handling**: Comprehensive error states and user feedback

## 📈 Future Enhancements

- Email notifications for new feedback
- Feedback analytics and reporting
- Bulk feedback operations
- Employee self-assessment features
- Integration with HR systems
- Advanced filtering and search

## 🤝 Contributing

This project follows clean coding practices:
- Modular component architecture
- TypeScript for type safety
- Comprehensive error handling
- Responsive design principles
- RESTful API design

## 📄 License

This project is built for educational and demonstration purposes.