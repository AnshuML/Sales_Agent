# Installation Guide

## Quick Install

### Method 1: Install from Source (Recommended for Development)

```bash
# Clone/download the repository
cd multi_agent_sales_system

# Install in development mode
pip install -e .
```

### Method 2: Regular Installation

```bash
cd multi_agent_sales_system
pip install .
```

### Method 3: Install with Dev Dependencies

```bash
pip install -e ".[dev]"
```

## Verify Installation

```bash
# Check if package is installed
pip show multi-agent-sales-analysis

# Run the CLI
sales-agent

# Or use as Python module
python -m sales_agent.main
```

## Platform-Specific Notes

### Windows

```powershell
# Use PowerShell or Command Prompt
cd multi_agent_sales_system
pip install -e .
```

### Mac/Linux

```bash
cd multi_agent_sales_system
pip install -e .
```

## Dependencies

All dependencies will be automatically installed:
- LangChain & LangGraph
- Google Gemini AI
- Pandas, NumPy
- OpenPyXL (Excel support)
- Matplotlib, Seaborn (Visualization)
- Google Auth libraries

## Configuration

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Edit `.env` and add:**
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

3. **(Optional) Google Drive Setup:**
   - Follow `GOOGLE_DRIVE_SETUP.md`
   - Place `credentials.json` in `credentials/` folder

## Troubleshooting

**Issue:** `ModuleNotFoundError`
```bash
# Solution: Reinstall
pip uninstall multi-agent-sales-analysis
pip install -e .
```

**Issue:** Import errors
```bash
# Solution: Check Python path
python -c "import sys; print(sys.path)"
pip list | grep multi-agent
```

**Issue:** Missing dependencies
```bash
# Solution: Reinstall with dependencies
pip install -e . --force-reinstall
```

## Uninstall

```bash
pip uninstall multi-agent-sales-analysis
```

## Next Steps

- Read [README.md](README.md) for usage
- Check [examples/](examples/) for code samples
- See [GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md) for OAuth

---

**Need help?** Open an issue on GitHub!
