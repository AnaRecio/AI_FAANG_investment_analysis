import os
import warnings
from datetime import datetime
from faang_investment_crew.crew import FaangInvestmentCrew

# Suppress a known spacy-related warning from pysbd (used in some LLM pipelines)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Entrypoint for running the full FAANG investment analysis pipeline.
    Executes all research, analysis, and reporting tasks via CrewAI.
    """
    output_markdown_path = "reports/faang_report.md"

    # Ensure the output directory exists before report generation
    os.makedirs(os.path.dirname(output_markdown_path), exist_ok=True)

    # Define input context passed to agents
    inputs = {
        'topic': 'FAANG Q1 2025',
        'current_year': str(datetime.now().year)
    }

    print("\n🚀 Running the FAANG Investment Crew...")
    result = FaangInvestmentCrew().crew().kickoff(inputs=inputs)

    print("\n✅ FAANG Investment Report generated successfully.")
    print(result)

# Run the pipeline if executed as the main script
if __name__ == "__main__":
    run()
