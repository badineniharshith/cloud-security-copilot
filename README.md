```markdown
# 📊 Online Survey System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![React](https://img.shields.io/badge/React-18.2.0-61dafb)
![Node.js](https://img.shields.io/badge/Node.js-22.16.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.2-336791)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation Guide](#installation-guide)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [CRUD Operations](#crud-operations)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Project Overview

The **Online Survey System** is a full-stack web application that allows users to create, manage, and analyze surveys efficiently. Built with modern web technologies, it provides an intuitive interface for creating surveys with multiple question types, collecting responses, and viewing real-time analytics.

### Purpose
This project was developed as a coursework requirement to demonstrate proficiency in:
- Full-stack web development
- Database design and management
- RESTful API development
- User authentication and authorization
- CRUD operations implementation

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Authentication** | Register, Login, and Session Management |
| 📝 **Create Surveys** | Create surveys with multiple question types |
| 📋 **Take Surveys** | Users can respond to available surveys |
| 📊 **Results Analytics** | View response statistics and percentages |
| 🎛️ **Dashboard** | Manage all your surveys in one place |
| ✏️ **Edit Surveys** | Update survey titles, descriptions, and status |
| 🗑️ **Delete Surveys** | Remove unwanted surveys |
| 👥 **User Profiles** | Personalized user experience |

### Question Types Supported

- ✅ **Text Answer** - Open-ended responses
- ✅ **Multiple Choice** - Single select from options
- ✅ **Rating Scale** - 1 to 5 rating system

---

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React.js | 18.2.0 | UI Framework |
| React Router DOM | 6.14.0 | Navigation |
| Axios | 1.4.0 | HTTP Client |
| CSS3 | - | Styling |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 22.16.0 | Runtime Environment |
| Express.js | 4.18.2 | Web Framework |
| PostgreSQL | 16.2 | Database |
| pg | 8.11.3 | PostgreSQL Client |

### Development Tools
- **VS Code** - Code Editor
- **pgAdmin 4** - Database Management
- **Git** - Version Control
- **Postman** - API Testing

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser (Client)                         │
│                   React.js Application                       │
│                     http://localhost:3000                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ HTTP/REST API
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Backend Server                            │
│                  Node.js + Express.js                        │
│                     http://localhost:5000                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ SQL Queries
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   PostgreSQL Database                        │
│                        surveysystem                          │
│                                                              │
│    ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐    │
│    │  users  │  │ surveys │  │questions │  │responses │    │
│    └─────────┘  └─────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Installation Guide

### Prerequisites

Before you begin, ensure you have the following installed:

| Software | Minimum Version | Download Link |
|----------|----------------|---------------|
| Node.js | v16.0+ | https://nodejs.org/ |
| PostgreSQL | v14.0+ | https://www.postgresql.org/ |
| npm | v8.0+ | Comes with Node.js |
| Git | Latest | https://git-scm.com/ |

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/online-survey-system.git
cd online-survey-system
```

### Step 2: Setup Database

Open **SQL Shell (psql)** or Command Prompt:

```bash
psql -U postgres
```

Enter your PostgreSQL password, then run:

```sql
CREATE DATABASE surveysystem;
\c surveysystem;
```

Create the tables:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Surveys table
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- Questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'text',
    options TEXT[]
);

-- Responses table
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    answer TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Insert admin user:

```sql
INSERT INTO users (name, email, password, role) 
VALUES ('Admin', 'admin@survey.com', 'admin123', 'admin');
```

### Step 3: Setup Backend

```bash
cd backend
npm install
```

Create `.env` file in backend folder:

```env
DB_USER=postgres
DB_HOST=localhost
DB_NAME=surveysystem
DB_PASSWORD=your_password
DB_PORT=5432
PORT=5000
```

### Step 4: Setup Frontend

```bash
cd ../frontend
npm install
npm install react-router-dom axios
```

---

## 📁 Project Structure

```
online-survey-system/
│
├── backend/
│   ├── server.js          # Main backend server
│   ├── package.json       # Backend dependencies
│   └── .env               # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CreateSurvey.jsx
│   │   │   ├── TakeSurvey.jsx
│   │   │   └── Results.jsx
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── README.md
│
└── database/
    └── schema.sql         # Database schema
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│      users      │
├─────────────────┤
│ id (PK)         │◄──────┐
│ name            │       │
│ email (UNIQUE)  │       │
│ password        │       │
│ role            │       │
│ created_at      │       │
└────────┬────────┘       │
         │                │
         │ 1              │
         │                │
         │ N              │
         ▼                │
┌─────────────────┐       │
│     surveys     │       │
├─────────────────┤       │
│ id (PK)         │       │
│ title           │       │
│ description     │       │
│ created_by (FK)─┼───────┘
│ created_at      │
│ status          │
└────────┬────────┘
         │
         │ 1
         │
         │ N
         ▼
┌─────────────────┐       ┌─────────────────┐
│    questions    │       │    responses    │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ survey_id (FK)──┼──────►│ survey_id (FK)──┼──────► surveys
│ question_text   │       │ question_id(FK)─┼──────► questions
│ question_type   │       │ user_id (FK)────┼──────► users
│ options         │       │ answer          │
└─────────────────┘       │ submitted_at    │
                          └─────────────────┘
```

### Tables Description

| Table | Description | Key Fields |
|-------|-------------|------------|
| **users** | Stores user information | id (PK), email (UNIQUE), role |
| **surveys** | Stores survey metadata | id (PK), created_by (FK to users) |
| **questions** | Stores survey questions | id (PK), survey_id (FK to surveys) |
| **responses** | Stores user answers | id (PK), survey_id, question_id, user_id |

---

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/register` | Register new user | `{name, email, password}` |
| POST | `/api/login` | User login | `{email, password}` |
| GET | `/api/users` | Get all users | - |

### Survey Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/surveys` | Get all surveys | - |
| GET | `/api/surveys/:id` | Get specific survey | - |
| POST | `/api/surveys` | Create new survey | `{title, description, created_by, questions}` |
| PUT | `/api/surveys/:id` | Update survey | `{title, description, status}` |
| DELETE | `/api/surveys/:id` | Delete survey | - |
| GET | `/api/my-surveys/:userId` | Get user's surveys | - |

### Response Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/responses` | Submit responses | `{survey_id, user_id, answers}` |
| GET | `/api/results/:surveyId` | Get survey results | - |

---

## 🚀 How to Run

### Step 1: Start Backend Server

Open **Terminal 1**:

```bash
cd backend
node server.js
```

**Expected Output:**
```
Server running on http://localhost:5000
Connected to PostgreSQL database
```

### Step 2: Start Frontend Server

Open **Terminal 2**:

```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view frontend in the browser.
Local: http://localhost:3000
```

### Step 3: Access the Application

Open your browser and go to:
```
http://localhost:3000
```

### Step 4: Test the Application

1. **Register** a new account
2. **Login** with your credentials
3. **Create** a new survey
4. **Take** a survey
5. **View** results in dashboard

---


## 🔄 CRUD Operations

| Operation | Implementation | Location |
|-----------|----------------|----------|
| **C**reate | Create new survey | Create Survey Page |
| **R**ead | View all surveys | Home Page / Dashboard |
| **U**pdate | Edit survey details | Dashboard (Edit button) |
| **D**elete | Remove survey | Dashboard (Delete button) |

---

## 🧪 Testing

### Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@survey.com | admin123 |
| User | (your registered email) | (your password) |

### Test Cases

| Test ID | Test Case | Expected Result |
|---------|-----------|-----------------|
| TC-01 | Register with new email | User created successfully |
| TC-02 | Register with existing email | Error message |
| TC-03 | Login with correct credentials | Redirect to home |
| TC-04 | Login with wrong password | Error message |
| TC-05 | Create survey | Survey saved to database |
| TC-06 | Edit survey | Changes reflected |
| TC-07 | Delete survey | Survey removed |
| TC-08 | Take survey | Responses saved |
| TC-09 | View results | Statistics displayed |
| TC-10 | Logout | Session cleared |

---

## 🔮 Future Enhancements

- [ ] Email notifications for new surveys
- [ ] Export results to CSV/Excel
- [ ] Charts and graphs for visual analytics
- [ ] Password encryption with bcrypt
- [ ] Forgot password functionality
- [ ] Survey templates
- [ ] Anonymous responses option
- [ ] Mobile application (React Native)
- [ ] Social media sharing
- [ ] Response validation rules

---

## 🐛 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Database connection failed | Check PostgreSQL is running and password is correct |
| Port 5000 already in use | Run `net stop winnat` or change port in server.js |
| Module not found | Run `npm install` in respective directory |
| CORS error | Ensure backend has `app.use(cors())` |
| Registration fails | Check backend terminal for error details |

---

## 👨‍💻 Contributors

| Name | Roll Number | Role |
|------|-------------|------|
| BADINENI HARSHITH | 2023001778 | Full Stack Developer |

---

## 📄 License

This project is developed for academic purposes as part of coursework requirement.

---

## 🙏 Acknowledgments

- React.js Documentation
- Node.js Documentation
- PostgreSQL Documentation
- Course Instructor for guidance

---

## 📞 Contact

For any queries or support:
- **Email:** badineniharshith.49@gmail.com

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 10-04-2026 | Initial release |

---

**⭐ If you found this project helpful, please star the repository!**

```
