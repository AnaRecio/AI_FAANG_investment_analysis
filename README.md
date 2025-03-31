# 🧠 AI FAANG Investment Analysis

An autonomous AI multi-agent system built with [CrewAI](https://github.com/joaomdmoura/crewai), designed to research, analyze, and generate professional investment reports for FAANG companies (Meta, Apple, Amazon, Netflix, Google).

This project uses LLMs, real-time financial data, sentiment analysis, and automated report generation to deliver polished Markdown and HTML reports with actionable insights.

## 🚀 Installation

> **Requirements:** Python ≥ 3.10 and < 3.13 and [UV](https://docs.astral.sh/uv/)

1. **Install UV**
   ```bash
   pip install uv
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/AnaRecio/AI_FAANG_investment_analysis.git
   cd faang_investment_crew
   ```

3. **Install Dependencies**
   ```bash
   crewai install
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your-openai-key
   SERPER_API_KEY=your-serper-key
   ```
   - An example is provided in `.env.example`

## ▶️ Running the Crew

Launch your agentic workflow:
```bash
crewai run
```

This will:
- 🔎 Research each FAANG company
- 📈 Analyze financial metrics and news sentiment
- 📄 Generate a full Markdown and HTML report in the `output/` folder

## 🧩 Agent Roles

Defined in `config/agents.yaml`:

### Researcher
- Gathers live stock data from Yahoo Finance
- Collects relevant news using Serper.dev

### Analyst
- Analyzes collected data
- Performs sentiment scoring
- Generates P/E and price ranges
- Assigns recommendations

### Reporting Analyst
- Generates investor-facing reports
- Creates Markdown + HTML output
- Includes tables, charts, and insights

## 📁 Project Structure

```
faang_investment_crew/
├── .env.example                # Template for required API keys
├── pyproject.toml             # Project + dependency metadata
├── requirements.txt           # (Optional) fallback dependencies
├── uv.lock                    # UV package lock file               
└── src/
    └── faang_investment_crew/
        ├── config/
        │   ├── agents.yaml    # Agent configurations
        │   └── tasks.yaml     # Task definitions
        ├── tools/
        │   ├── markdown_generator.py
        │   ├── serper_search_tool.py
        │   └── yahoo_finance.py
        ├── knowledge/         # Stores historical reports
        ├── main.py            # Entry point for `crewai run`
        └── crew.py            # Crew definition (agents + tasks)
```

## 📊 Output

The generated report includes:

### Executive Summary
- Comprehensive analysis of FAANG companies' performance
- Market sentiment evaluation

### Comparative Analysis
- Stock Price
- Market Cap
- P/E Ratio
- 52-week Low & High
- Sentiment
- Recommendation

### Detailed Sections
- Individual company assessments
- Strategic investment insights
- Sources list for traceability

### File Outputs
- Markdown report: `output/faang_report_<timestamp>.md`
- HTML report: `output/faang_report_<timestamp>.html`
  - Includes embedded tables and charts

## 📌 Technical Notes

### Dependencies
- Core: `crewai`
- Data: `yfinance`
- Web & Parsing: `requests`, `beautifulsoup4`
- Report Generation: `markdown2`, `weasyprint`

### Configuration
- API Keys managed via `.env` (ignored in version control)
- Fonts for PDF generation in `assets/fonts/`
- Historical reports stored in `knowledge/`



