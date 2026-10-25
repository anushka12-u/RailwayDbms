# RailwayDbms

RailConnect is a railway management system built with **FastAPI**, **MySQL**, and **Streamlit**. It provides a web interface for managing trains, passengers, ticket bookings, and payments.

## Features

- Train management
- Passenger management
- Ticket booking and booking history
- Payment management
- Railway dashboard and analytics
- FastAPI backend with MySQL database
- Streamlit frontend

## Project Structure

```text
RailwayDbms/
├── backend/        # FastAPI application and API routes
├── database/       # MySQL database schema
├── frontend/       # Streamlit application
├── requirements.txt
└── README.md
```

## Requirements

Install the following before running the application:

- Python 3.10 or newer
- MySQL Server 8.0 or newer
- Git

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/anushka12-u/RailwayDbms.git
   cd RailwayDbms
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the **repository root**. Do not commit this file to GitHub.

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=railway_management
```

### Backend variables

| Variable | Required | Description | Example |
|---|---:|---|---|
| `DB_HOST` | Yes | MySQL server hostname or IP address | `localhost` |
| `DB_USER` | Yes | MySQL username | `root` |
| `DB_PASSWORD` | Yes | MySQL password | `your_mysql_password` |
| `DB_NAME` | Yes | MySQL database name | `railway_management` |

### Frontend variable

The Streamlit frontend uses `RAILWAY_API_URL` to locate the FastAPI backend. If it is not provided, it defaults to `http://127.0.0.1:8000`.

```env
RAILWAY_API_URL=http://127.0.0.1:8000
```

For local development, the API default is sufficient. If you use a different host or port, set the variable in the terminal before starting Streamlit.

**Windows PowerShell:**

```powershell
$env:RAILWAY_API_URL="http://127.0.0.1:8000"
```

**macOS/Linux:**

```bash
export RAILWAY_API_URL=http://127.0.0.1:8000
```

> Never commit real database passwords, API keys, or other secrets. The repository's `.gitignore` excludes `.env` files.

## Database Setup

1. Start your MySQL server.

2. Run the schema file using the MySQL client:

   ```bash
   mysql -u root -p < database/schema.sql
   ```

   Alternatively, open `database/schema.sql` in MySQL Workbench and execute it.

3. Confirm that the database name in `.env` matches the database created by the schema:

   ```env
   DB_NAME=railway_management
   ```

The schema creates the following tables:

- `trains`
- `passengers`
- `bookings`
- `payments`

## Running the Application

The backend and frontend run as separate processes. Open two terminals and activate the virtual environment in both.

### 1. Start the FastAPI backend

From the repository root:

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs
- ReDoc documentation: http://127.0.0.1:8000/redoc

### 2. Start the Streamlit frontend

Open a second terminal, activate the virtual environment, and run:

**Windows PowerShell:**

```powershell
$env:RAILWAY_API_URL="http://127.0.0.1:8000"
streamlit run frontend/app.py
```

**macOS/Linux:**

```bash
export RAILWAY_API_URL=http://127.0.0.1:8000
streamlit run frontend/app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## API Health Check

After starting the backend, visit http://127.0.0.1:8000 or run:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"message":"Railway Management System API is running"}
```

## Troubleshooting

### Cannot connect to MySQL

- Confirm that MySQL is running.
- Check `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in `.env`.
- Confirm that `database/schema.sql` has been executed.
- Make sure the MySQL user has permission to access `railway_management`.

### Frontend cannot connect to the API

- Confirm that the FastAPI backend is running.
- Check that `RAILWAY_API_URL` matches the backend URL and port.
- Start the backend before opening the Streamlit frontend.

### Import or dependency errors

Make sure the virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## Development Notes

- Backend entry point: `backend/main.py`
- Frontend entry point: `frontend/app.py`
- Database schema: `database/schema.sql`
- Backend database configuration: `backend/database.py`

## License

This project currently does not specify a license.
