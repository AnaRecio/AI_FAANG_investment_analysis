import os
import json
import markdown2 as markdown
import webbrowser
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

def reporting_task_callback(task_output, output_file="faang_report", chart_path=None, auto_open=True):
    """
    Callback for the final reporting agent task.
    Parses the output (expected to be JSON), formats it into Markdown, and generates both .md and .html reports.
    """
    print("[✅] Generating report from Investment Report Specialist...")

    try:
        # Support both structured and plain outputs depending on agent behavior
        output_content = task_output.output if hasattr(task_output, 'output') else task_output
        report_data = json.loads(output_content)
        markdown_text = format_report_to_markdown(report_data)
    except Exception as e:
        # If parsing fails, log the raw output and fallback to treating it as plain text
        print("[❌] Failed to parse task output as JSON.")
        print("Raw output:", output_content)
        markdown_text = str(output_content)

    return generate_markdown_and_html(markdown_text, output_file, chart_path, auto_open)

def format_report_to_markdown(data: dict) -> str:
    """
    Formats structured report data into Markdown content.
    Handles section headers, financial tables, insights, and source attribution.
    """
    sections = []

    if "executive_summary" in data:
        sections.append(f"# Executive Summary\n{data['executive_summary']}\n")

    if "comparative_financial_table" in data:
        sections.append("## Comparative Financial Table\n")
        table = data["comparative_financial_table"]
        headers = ["Company", "Stock Price", "Market Cap", "P/E Ratio", "Sentiment", "Recommendation"]
        header_row = "| " + " | ".join(headers) + " |"
        separator = "|" + "---|" * len(headers)
        rows = []

        for company, metrics in table.items():
            row = [
                company,
                metrics.get("Stock Price", "Data Not Found"),
                metrics.get("Market Cap", "Data Not Found"),
                metrics.get("P/E Ratio", "Data Not Found"),
                metrics.get("Sentiment", "Data Not Found"),
                metrics.get("Recommendation", "Data Not Found")
            ]
            rows.append("| " + " | ".join(row) + " |")

        sections.append(header_row)
        sections.append(separator)
        sections.extend(rows)
        sections.append("")

    if "company-specific_assessments" in data:
        sections.append("## Company-Specific Assessments\n")
        for company, assessment in data["company-specific_assessments"].items():
            sections.append(f"### {company}")
            for k, v in assessment.items():
                sections.append(f"- **{k}**: {v}")
            sections.append("")

    if "strategic_investment_insights" in data:
        insights = data["strategic_investment_insights"]
        sections.append("## Strategic Investment Insights\n")

        if "Recommendations" in insights:
            sections.append("### Recommendations")
            for company, reco in insights["Recommendations"].items():
                sections.append(f"- **{company}**: {reco}")
            sections.append("")

        if "Reasoning" in insights:
            sections.append(f"### Reasoning\n{insights['Reasoning']}\n")

    if "sources" in data:
        sections.append("## Sources\n")
        for source in data["sources"]:
            sections.append(f"- [{source['title']}]({source['url']})")

    sections.append("\n> *Disclaimer: This report is for informational purposes only and does not constitute financial advice.*\n")

    return "\n".join(sections)

def generate_markdown_and_html(markdown_text: str, filename_base: str, chart_path: str = None, auto_open: bool = True):
    """
    Converts the Markdown text into an HTML file with optional embedded chart image.
    Saves both .md and .html versions with a timestamped filename.
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{filename_base}_{now}.md"
    html_path = output_dir / f"{filename_base}_{now}.html"

    # Write Markdown file to disk
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    # Convert Markdown to HTML
    html_body = markdown.markdown(markdown_text, extras=["tables", "fenced-code-blocks"])
    soup = BeautifulSoup(html_body, "html.parser")

    # Full HTML template with inline styles for clean rendering
    full_html = f"""
    <html>
    <head>
        <meta charset=\"UTF-8\">
        <title>FAANG Investment Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 2rem; line-height: 1.6; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #f5f5f5; }}
            h1, h2, h3 {{ color: #333; }}
            img {{ margin-top: 20px; }}
            blockquote {{ font-style: italic; color: #555; border-left: 4px solid #ddd; margin: 1rem 0; padding-left: 1rem; }}
        </style>
    </head>
    <body>{soup}</body>
    </html>
    """

    # Write final HTML file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[✅] Markdown report saved to {md_path}")
    print(f"[✅] HTML report saved to {html_path}")
