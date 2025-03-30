import warnings
from datetime import datetime
from faang_investment_crew.crew import FaangInvestmentCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the FAANG investment analysis crew."""
    inputs = {
        'topic': 'FAANG Q1 2025',
        'current_year': str(datetime.now().year)
    }
    FaangInvestmentCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
