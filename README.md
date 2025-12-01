# ohtuvarasto

<a href="https://github.com/eemikh/ohtuvarasto/actions/"><img src="https://github.com/eemikh/ohtuvarasto/actions/workflows/main.yml/badge.svg" alt="GHA badge"/></a>

<a href="https://codecov.io/github/eemikh/ohtuvarasto"><img src="https://codecov.io/github/eemikh/ohtuvarasto/graph/badge.svg?token=NKJLV9XJYM"/></a>

## Varasto Web UI

A Flask-based web interface for managing multiple varastos (warehouses).

### Features

- Create multiple varastos with custom capacity
- Add and remove inventory
- Visual progress indicators showing capacity
- Real-time inventory tracking
- Error handling and validation

### Running the Application

1. Install dependencies:
```bash
pip install flask
```

2. Run the application:
```bash
cd src
python3 app.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000/`

### Development

Run with debug mode (development only):
```bash
FLASK_DEBUG=true python3 app.py
```

### Testing

Run the test suite:
```bash
python3 -m pytest src/tests/
```
