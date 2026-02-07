# Contributing to Multi-Agent Sales Analysis System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multi-agent-sales-analysis.git
cd multi-agent-sales-analysis
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**
```bash
pip install -e ".[dev]"
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Project Structure

```
multi_agent_sales_system/
├── src/
│   └── sales_agent/          # Main package
│       ├── agents/           # Multi-agent system
│       ├── data_sources/     # Data connectors
│       ├── functions/        # Analysis functions
│       ├── visualizations/   # Chart creation
│       └── utils/            # Utilities
├── tests/                    # Test suite
├── docs/                     # Documentation
├── examples/                 # Example usage
└── pyproject.toml            # Project config
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for all public functions
- Maximum line length: 100 characters

**Format code with Black:**
```bash
black src/ tests/
```

**Check with Flake8:**
```bash
flake8 src/ tests/
```

## Testing

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_data_ops.py
```

**Run with coverage:**
```bash
pytest --cov=sales_agent tests/
```

## Adding New Features

1. **Create a new branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Write your code**
   - Add new functionality
   - Write tests
   - Update documentation

3. **Test your changes**
```bash
pytest
black src/
flake8 src/
```

4. **Commit your changes**
```bash
git add .
git commit -m "Add: Description of your feature"
```

5. **Push and create Pull Request**
```bash
git push origin feature/your-feature-name
```

## Adding New Data Sources

To add a new data source (e.g., PostgreSQL):

1. Create `src/sales_agent/data_sources/postgresql.py`
2. Implement connector class
3. Add detection logic to `data_retrieval_agent.py`
4. Update documentation
5. Add tests

## Adding New Analysis Functions

1. Add function to appropriate module in `src/sales_agent/functions/`
2. Import in `analysis_agent.py`
3. Update function selection logic
4. Write tests in `tests/test_<module>.py`
5. Update documentation

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md
- Add docstrings to all new functions
- Update type hints

## Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what & why
- **Tests**: Include tests for new features
- **Documentation**: Update relevant docs
- **Code Style**: Pass Black & Flake8

## Reporting Issues

When reporting bugs, include:
- Python version
- OS (Windows/Mac/Linux)
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Questions?

Feel free to open an issue for questions or discussions!

---

**Thank you for contributing!** 🎉
