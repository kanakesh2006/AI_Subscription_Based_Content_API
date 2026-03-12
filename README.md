# AI Subscription-Based Content API

A robust backend API built with FastAPI and PostgreSQL for a premium content platform.

## Features

- **User Authentication**: Secure JWT-based registration and login.
- **Subscription Management**: Upgrade from Free to Premium (simulated payment).
- **Access Control**: Role-based protection for premium content.
- **Activity Logging**: Automated logging of all premium content access.
- **Subscription Expiry**: Automated role downgrade after 30 days.
- **Admin Dashboard**: View access logs and export CSV usage reports.

## Prerequisites

- Python 3.9+
- PostgreSQL

## Quick Start

1. **Clone the repository**
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**:
   Create a `.env` file based on the provided configuration:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=yoursecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   GROQ_API_KEY=yoursecretkey
   ```
5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

![All End Points](assets/images/Screenshot%202026-03-12%20193800.png)

### Authentication
- `POST /register`: Create a new account.
- `POST /login`: Authenticate and receive a JWT.
- `GET /me`: View current user profile and role.

### Subscription
- `POST /subscription/upgrade`: Upgrade account to Premium (Simulated).

### Content
- `GET /content/free`: Access public content.
- `GET /content/premium`: Access protected premium content (Requires Premium).

### Admin
- `GET /admin/access-logs`: View all platform usage logs.
- `GET /admin/reports`: Download CSV usage report.

### AI Features (Admin Only)
- `GET /admin/ai/log-analysis`: Automated AI-driven insights from platform logs.
- `POST /admin/ai/query`: Ask natural language questions about user activity.
    - Example: `{"question": "Who is the most active premium user?"}`

- AI Log Analysis using LLMs (Groq) :

![log analysis](assets/images/Screenshot%202026-03-12%20193429.png)

- Natural Language Query :

Question :

![question](assets/images/Screenshot%202026-03-12%20193518.png)

Answer :

![answer](assets/images/Screenshot%202026-03-12%20193604.png)



## Documentation
Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.
