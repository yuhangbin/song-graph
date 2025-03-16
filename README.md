# Song-Graph

A Music Metadata Analysis and Visualization Project that collects, analyzes, and visualizes music data.

## Project Structure

```
.
├── src/
│   └── song_graph/     # Source code
│       ├── __init__.py
│       └── main.py
├── tests/             # Test files
├── requirements.txt   # Project dependencies
├── .gitignore        # Git ignore rules
└── README.md         # Project documentation
```

## Database Schema

### Songs Table
TBD - Will contain song metadata

### artists roles Table
TBD - Will contain producer information

## Agent Workflow

1. Collect music metadata
2. Check data
3. Evaluation data
4. Convert to visual format
5. Repeat

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

## License

MIT
