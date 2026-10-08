# flow-forge-be

This is a FastAPI project that serves as the backend for FlowForge. It provides the necessary APIs and services to support the FlowForge platform.

## ⚙️ Tech Stack

| Category                  | Technologies                    | Purpose                                           |
| :------------------------ | :------------------------------ | :------------------------------------------------ |
| **Core Language**         | Python                          | Primary programming language.                     |
| **Web Framework**         | FastAPI                         | Building the asynchronous API endpoints.          |
| **Data Modeling**         | SQLModel, Pydantic              | Data validation and database object definitions.  |
| **Database**              | PostgreSQL                      | Primary relational database.                      |
| **Persistence/Migration** | Alembic, SQLModel               | Database migrations and interaction.              |
| **AI Workflow**           | LangChain, LangGraph, MistralAI | Complex, stateful AI agent workflows.             |
| **Vector Store**          | LangChain-Chroma                | Implementing vector storage for AI retrieval.     |
| **Configuration**         | Pydantic-Settings               | Managing environment variables and configuration. |
| **Security**              | JWT, Passlib, Cryptography      | Authentication, password hashing, and encryption. |
| **Caching/Broker**        | Redis                           | Caching and message queuing.                      |

## 🚀 Getting Started

### Running the application

To run the application using `uv`, use the following command:

```bash
uv run fastapi run
```

To run in debug mode, you might use:

```bash
uv run fastapi dev
```

### Running tests

To run the tests, use the following command:

```bash
pytest
```
