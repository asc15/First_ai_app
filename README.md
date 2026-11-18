# Weather Agent

A command-line AI weather assistant built with LangChain, LangGraph, OpenWeatherMap, and PostgreSQL-backed conversation state.

The agent can:

- get weather by city
- detect the user's location when no city is provided
- remember conversation state using a PostgreSQL database
- keep running until the user types `exit` or `quit`

The main script is [weatherAgent.py](weatherAgent.py).

## Requirements

- Python 3.10 or later
- OpenWeatherMap API key
- KodeKloud AI API key or another OpenAI-compatible API key
- PostgreSQL or Supabase database connection string

## Setup

1. Open a terminal in the project folder.

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, the included `psycopg-binary` package provides the PostgreSQL runtime library needed by `langgraph-checkpoint-postgres`.

4. Create a `.env` file in the project root:

```env
OPEN_WEATHER_API_KEY=your_openweather_api_key
KODEKEY_API_KEY=your_kodekey_api_key
SUPABASE_URL=postgresql://username:password@host:5432/database
```

Use the direct PostgreSQL connection string from Supabase or PostgreSQL. Keep this file private and do not commit it to source control.

## Run the app

With the virtual environment active:

```powershell
python weatherAgent.py
```

Enter a weather question at the prompt:

```text
Ask your question:
```

Example questions:

```text
What is the weather in London?
How hot is it in New York right now?
What is the weather here?
```

Type `exit` or `quit` to close the application.

## How it works

- When the user provides a city, the agent calls the weather API directly.
- When no city is provided, the agent calls `get_location` to obtain the user's approximate location from their public IP address.
- The LLM uses the OpenAI-compatible endpoint configured in [weatherAgent.py](weatherAgent.py).
- `PostgresSaver` stores agent checkpoints and conversation state in PostgreSQL.
- `checkpointer.setup()` creates the required checkpoint tables if they do not already exist.

## Troubleshooting

### Missing PostgreSQL implementation

If Psycopg reports `no pq wrapper available`, reinstall the binary PostgreSQL dependencies:

```powershell
python -m pip install --upgrade "psycopg[binary]" psycopg-pool langgraph-checkpoint-postgres
```

Do not install a package named `libpq` with pip; it is not a standalone Python package.

### Database connection failure

Verify that:

- `SUPABASE_URL` is set in `.env`
- the database host and port are reachable
- the username and password are correct
- your database provider allows connections from your network
