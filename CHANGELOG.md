# Changelog

All notable changes to the Multi-Agent Sales Analysis System will be documented in this file.

## [1.0.0] - 2026-02-06

### Added
- Initial release of Multi-Agent Sales Analysis System
- Orchestrator agent for conversation management
- Data Retrieval Agent with Google Drive and local file support
- Analysis Agent with hybrid LLM + function approach
- Quarter sales calculation (Nov, Dec, Jan aggregation)
- Excel file read/write with new column addition
- Visualization module (bar, pie, scatter, box, line charts)
- Data operations: filter, group, pivot, merge
- Statistical analysis: growth rates, moving averages, outlier detection
- Conversational CLI interface
- Google Drive OAuth 2.0 integration
- Comprehensive documentation and setup guides

### Features
- Natural language query understanding via Google Gemini Pro
- Multi-turn conversational interface
- Automatic data source detection
- Intelligent column name detection
- Professional chart generation with Seaborn
- State management across conversation
- Fallback logic when LLM fails

### Supported Data Sources
- Google Drive (Google Sheets → Excel conversion)
- Local files (CSV, Excel, JSON)
- AWS S3 (planned)

### Documentation
- README.md with quick start guide
- GOOGLE_DRIVE_SETUP.md for OAuth configuration
- Comprehensive walkthrough documentation
- Test results and verification report

## [Unreleased]

### Planned Features
- AWS S3 integration
- Excel formula library (SUMIF, VLOOKUP, etc.)
- Streamlit web UI
- Additional LLM providers (OpenAI, Claude)
- Database connectors (MySQL, PostgreSQL)
- Scheduled report generation
- Email integration for automated reports
- Multi-file batch processing
