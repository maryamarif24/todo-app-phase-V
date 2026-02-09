# TodoApp - Phase III: Conversational AI Todos

A modern, full-stack todo application with conversational AI capabilities, built with Next.js frontend and FastAPI backend.

## Features

- ✅ User authentication and authorization
- ✅ Full CRUD operations for todos
- ✅ Priority management (High, Medium, Low)
- ✅ Due date tracking
- ✅ Real-time dashboard with statistics
- ✅ Responsive design with mobile support
- ✅ Conversational AI chatbot for task management
- ✅ Export functionality (CSV/JSON)
- ✅ Docker containerization
- ✅ CI/CD pipeline

## Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Better Auth** - Authentication

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Alembic** - Database migrations

### DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD
- **Husky + lint-staged** - Pre-commit hooks

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app-phase-III-chatbot
```

2. Start the services:
```bash
docker-compose -f infra/docker-compose.yml up --build
```

3. Open your browser to `http://localhost:3000`

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app-phase-III-chatbot
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set up your database and run migrations
uvicorn src.main:app --reload
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm run dev
```

4. Open your browser to `http://localhost:3000`

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATBOT_API_URL=http://localhost:8000/chat
```

### Backend
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

## API Documentation

When running locally, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
todo-app-phase-III-chatbot/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── auth/           # Authentication
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities
│   ├── Dockerfile
│   └── package.json
├── infra/                   # Infrastructure
│   └── docker-compose.yml
├── .github/workflows/       # CI/CD
└── README.md
```

## Development

### Code Quality
- Pre-commit hooks with Husky and lint-staged
- ESLint and Prettier for frontend
- Black and isort for backend
- TypeScript for type safety

### Testing
```bash
# Frontend
cd frontend
npm run lint
npm run type-check

# Backend
cd backend
pytest
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

## Deployment

### Vercel (Frontend)
1. Connect your GitHub repository to Vercel
2. Set environment variables
3. Deploy

### Railway/Heroku (Backend)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy

### Docker Deployment
```bash
docker-compose -f infra/docker-compose.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details
