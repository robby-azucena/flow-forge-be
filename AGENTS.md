# FlowForge Backend Context

This document serves as a guide for AI agents assisting with development in the `flow-forge-be` project. It outlines the architecture, key technologies, and development patterns.

## 🚀 Project Overview
The `flow-forge-be` project is a backend API service built using **Python** and **FastAPI**. It is designed to handle core business logic, user management, database interactions, and advanced AI workflows.

## ⚙️ Technical Stack & Dependencies
**Core Framework:**
- **Python:** The primary language.
- **FastAPI:** Used for building the asynchronous API endpoints.
- **SQLModel/Pydantic:** Used for data modeling and validation.

**Database & Persistence:**
- **PostgreSQL:** The primary relational database.
- **SQLModel:** Used for defining models and interacting with the database.
- **Alembic:** Used for database migrations (configuration located in `alembic.ini`).

**AI & Workflow (LangChain Ecosystem):**
- **LangChain/LangGraph:** Used for complex, stateful AI agent workflows.
- **LangChain-MistralAI:** Specifies Mistral AI as a supported LLM.
- **LangChain-Chroma:** Implements vector storage for AI retrieval components.
- **LangChain-Text-Splitters/Pypdf:** Utilities for processing documents and preparing data for the AI chain.

**Security & Configuration:**
- **Pydantic-Settings:** Used for managing configuration from environment variables (defined in `config/settings.py`).
- **Cryptography:** Used for secure operations like Fernet encryption.
- **Passlib & JWT:** Used for password hashing and JSON Web Token (JWT) handling in authentication (`auth/auth.py`).
- **Redis:** Used as a cache/message broker (defined in `config/settings.py`).

## 📂 Directory Structure & Responsibilities

| Directory/File | Purpose | Key Technologies |
| :--- | :--- | :--- |
| `main.py` | Application entry point. Sets up FastAPI, registers middleware (CORS, Session Handling), and initializes components. | FastAPI |
| `config/` | Central configuration management. | Pydantic-Settings, `config/settings.py` |
| `config/settings.py` | Holds global application settings (DB strings, secret keys, Redis URLs, etc.) loaded from a `.env` file. | `cryptography`, `pydantic_settings` |
| `models/` | Defines data structures (e.g., `user.py`) that map to database tables. | SQLModel |
| `services/` | Implements core business logic (e.g., `user.py`). Contains the "how-to" logic for features. | Python Classes |
| `auth/` | Handles all authentication and authorization logic. | Passlib, JWT, Cryptography |
| `repositories/` | (Implied) Data access layer responsible for querying/persisting data to the database. | SQLModel |
| `controllers/` | (Implied) API endpoint handlers that receive requests and delegate to services. | FastAPI |
| `utils/` | Generic helper functions (e.g., `system_check.py`, `session_handler.py`). | General Utilities |

## 📝 Coding Conventions & Workflow Notes

1.  **Configuration:** All environment-specific parameters (DB connections, API keys) must be loaded via environment variables and are centralized in `config/settings.py`.
2.  **Dependency Injection:** The application relies heavily on Dependency Injection (DI) provided by FastAPI (e.g., `Depends(db.get_session)` in `main.py`) to manage resources like database sessions.
3.  **Data Flow:** Requests flow from **Controller** $\rightarrow$ **Service** $\rightarrow$ **Repository** $\rightarrow$ **Database**.
4.  **AI Integration:** AI components are implemented using the LangChain stack, typically involving a pipeline that reads data (e.g., from files via `pypdf`), chunks it, stores it in Chroma, and then uses a chain (potentially managed by LangGraph) with an LLM (MistralAI) to generate results.

## ⚠️ Important Notes for AI Agents
- **Security:** Never bypass or modify authentication checks. Secrets are handled via `config/settings.py` and environment variables.
- **Migrations:** Database changes should always be managed via Alembic migrations.
- **Modularity:** Changes should be localized. For example, if modifying user logic, focus on `models/user.py` and `services/user.py` first, then check related controllers/endpoints.
