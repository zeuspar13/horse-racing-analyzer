# Horse Racing Analyzer

A comprehensive horse racing analysis tool that combines API data with AI predictions to provide race insights.

## Features

- Real-time race card data from The Racing API
- AI-powered race analysis using Claude
- PowerShell GUI interface for race viewing
- Database storage for race data
- Automated race analysis workflow

## Prerequisites

- Python 3.8+
- PowerShell 5.1+
- PostgreSQL database

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd horse-racing-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your API credentials:
  - THE_RACING_API_USERNAME
  - THE_RACING_API_PASSWORD
  - CLAUDE_API_KEY

4. Initialize the database:
```bash
alembic upgrade head
```

## Usage

### PowerShell GUI

Run the PowerShell GUI:
```powershell
./scripts/race_viewer.ps1
```

### API Server

Start the FastAPI server:
```bash
uvicorn src.app.main:app --reload
```

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Project Structure

```
horse-racing-analyzer/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── services/
│           ├── racing_api.py
│           ├── racing_post_service.py
│           └── claude_service.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_flow.py
│   ├── test_race_cards.py
│   └── test_racing_api.py
├── scripts/
│   └── race_viewer.ps1
├── .env
├── .env.example
├── requirements.txt
├── alembic.ini
├── README.md
└── LICENSE
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Racing API for race data
- Claude for AI analysis
- FastAPI for the backend framework
