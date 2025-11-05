# ModernAI Pro Project Organization

## System Architecture

```
+------------------+           +-------------------+           +------------------+
|                  |  HTTP/WS  |                   |   SQL     |                  |
|    Frontend      |<--------->|     Backend       |<--------->|    Database      |
|    (React)       |           |    (FastAPI)      |           |  (SQLAlchemy)    |
|                  |           |                   |           |                  |
+------------------+           +-------------------+           +------------------+
                                       |
                                       | API
                                       v
                              +-------------------+
                              |                   |
                              |  AI Services      |
                              | (Groq, OpenAI)    |
                              |                   |
                              +-------------------+
```

## Backend Structure

- **API Layer**: FastAPI with CORS, JWT middleware
- **Models**:
  - User: Authentication, roles, permissions
  - Learning: Lessons, content, user progress
  - Programming: Challenges, sessions, pair programming
  - Quiz: Assessments, surveys, analytics
  - Workshop: Workshop sessions, payments
- **Database**: SQL with Alembic migrations
- **AI Integration**: LLM services, vector database, chat memory

## Frontend Structure

- **State Management**: Context API (AuthContext)
- **Main Pages**:
  - WelcomeDashboard: User entry point
  - LearningPaths: Educational content
  - PairProgramming: Collaborative coding
  - Workshops: Live learning sessions
- **Shared Components**: Navigation, authentication guards

## AI Architecture

```
+-------------------+             +-------------------+
|                   |             |                   |
|    LLM Models     |<----------->|   Vector Database |
| (Azure, Groq)     |             |    (ChromaDB)     |
|                   |             |                   |
+-------------------+             +-------------------+
         ^                                 ^
         |                                 |
         v                                 v
+-------------------+             +-------------------+
|                   |             |                   |
|   Chat Memory     |<----------->|   API Endpoints   |
|                   |             |                   |
+-------------------+             +-------------------+
```

## Implementation Status

- **Complete**: Authentication, database models, basic UI
- **In Progress**: AI integration, workshop functionality
- **Planned**: Real-time collaboration, adaptive learning