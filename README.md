# Multi-Agent Sales Analysis System

A conversational multi-agent system that retrieves## ✨ Key Features

- **🤖 Multi-Agent Orchestration**: Specialized agents for coordination, data retrieval, and analysis.
- **🧠 Advanced Analysis Super-Agent**:
  - **"Excel Expert" Mode**: Understands complex queries like "Compare Q1 vs Q2 sales for Region X".
  - **Dynamic Code Generation**: Writes custom Pandas code to solve *any* data problem.
  - **Proactive Insights**: Automatically detects trends, outliers, and key metrics on file load.
- **🔌 Multi-Source Data Retrieval**:
  - **Google Drive**: Seamlessly download files from shared links.
  - **Local Files**: direct analysis of local datasets.
  - **AWS S3**: (Coming soon) Enterprise storage support.
- **📊 Intelligent Visualization**: Automatically generates relevant charts (Bar, Line, Scatter, Pie) based on data context.
- **💾 Auto-Writeback**: Adds calculated results (e.g., "Quarter_Sales" column) directly to your Excel file.
- **💬 Conversational Interface**: Natural language queries

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Google Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. (Optional) Set Up Google Drive

If using Google Drive:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google Drive API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download `credentials.json` and place in `credentials/` folder

### 4. Run the System

```bash
python main.py
```

## 💡 Example Usage

```
🎯 What would you like to analyze?
User: Show me this quarter's sales (Nov, Dec, Jan)

🤖 Assistant: Where is your data stored?
  1️⃣ Google Drive (share the link)
  2️⃣ Local file (provide file path)

User: https://docs.google.com/spreadsheets/d/1xABC.../edit

🤖 Assistant:
✅ Successfully downloaded file from Google Drive!
📄 File: sales_data.xlsx

✅ Quarter Sales Calculated!
📊 Months: Nov, Dec, Jan
💰 Total Sales: 125,450.00
📄 Added column 'Quarter_Sales' to file
💾 Output file: sales_data_with_quarter_sales.xlsx
```

## 📁 Project Structure

```
multi_agent_sales_system/
├── agents/
│   ├── orchestrator.py        # Main coordinator
│   ├── data_retrieval_agent.py # Data source handler
│   └── analysis_agent.py      # Hybrid analysis engine
├── data_sources/
│   ├── google_drive.py        # Google Drive integration
│   └── local_storage.py       # Local file handler
├── functions/
│   ├── data_ops.py            # Data operations
│   ├── statistics.py          # Statistical analysis
│   └── data_manipulation.py   # Data transformation
├── visualizations/
│   └── charts.py              # Chart creation
├── utils/
│   ├── config.py              # Configuration
│   └── conversation_state.py  # State management
└── main.py                    # CLI entry point
```

## 🛠️ Technology Stack

- **LLM**: Google Gemini Pro (via LangChain)
- **Data**: Pandas, NumPy, OpenPyXL
- **Visualization**: Matplotlib, Seaborn
- **Cloud**: Google Drive API, AWS Boto3 (S3)

## 📋 Available Functions

### Data Operations
- Read CSV, Excel, JSON
- Filter, group, pivot data
- Merge datasets
- Calculate insights

### Statistics
- Quarter/period sales calculation
- Growth rates (MoM, QoQ, YoY)
- Descriptive statistics
- Moving averages
- Outlier detection

### Data Manipulation
- Add/populate columns
- Write to Excel
- Create derived metrics (profit margin, etc.)

### Visualizations
- Bar charts, pie charts, scatter plots
- Box plots, line charts, heatmaps

## 🤝 Contributing

This is a demo project. Feel free to extend with:
- More data sources (S3, databases)
- Additional LLM providers
- More analysis functions
- Streamlit web UI

## 📄 License

MIT License - see LICENSE file for details.

---

Built with ❤️ using LangChain, Google Gemini, and Python
