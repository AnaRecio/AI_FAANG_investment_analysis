import os
import webbrowser
from faang_investment_crew.crew import FaangInvestmentCrew

def generate_and_open_report(output_markdown_path="reports/faang_report.md"):
    # Ensure the reports folder exists
    os.makedirs(os.path.dirname(output_markdown_path), exist_ok=True)

    # Run the crew to generate report
    inputs = {
        "topic": "FAANG Q1 2025",
        "current_year": "2025"
    }

    print("🚀 Running the FAANG Investment Crew...")
    result = FaangInvestmentCrew().crew().kickoff(inputs=inputs)

    # Print/log final result
    print(result)

    # Derive HTML path from markdown
    html_path = output_markdown_path.replace(".md", ".html")
    full_path = os.path.abspath(html_path)

    if os.path.exists(full_path):
        print(f"✅ Report generated: {full_path}")
        webbrowser.open(f"file://{full_path}")
    else:
        print("⚠️ HTML report was not found.")
