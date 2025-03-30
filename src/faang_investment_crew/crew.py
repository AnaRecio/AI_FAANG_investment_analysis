from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from faang_investment_crew.tools.markdown_generator import reporting_task_callback
from faang_investment_crew.tools.serper_search_tool import serper_search
from faang_investment_crew.tools.yahoo_finance import YahooFinanceTool
import yaml
from dotenv import load_dotenv
import os

load_dotenv()

@CrewBase
class FaangInvestmentCrew():
    """CrewAI autonomous system for analyzing and reporting on FAANG companies."""

    def __init__(self):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        agents_path = os.path.join(package_dir, 'config', 'agents.yaml')
        tasks_path = os.path.join(package_dir, 'config', 'tasks.yaml')

        try:
            with open(agents_path, 'r', encoding='utf-8') as f:
                self.agents_config = yaml.safe_load(f)
            with open(tasks_path, 'r', encoding='utf-8') as f:
                self.tasks_config = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration files: {str(e)}")

    # === AGENTS ===
    @agent
    def researcher(self) -> Agent:
        config = self.agents_config['researcher']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    @agent
    def analyst(self) -> Agent:
        config = self.agents_config['analyst']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    @agent
    def reporting_analyst(self) -> Agent:
        config = self.agents_config['reporting_analyst']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    # === TOOLS ===
    @tool
    def serper_search(self):
        return serper_search
    
    @tool
    def yahoo_finance_data(self):
         return YahooFinanceTool()


    # === TASKS ===
    def _create_task(self, task_key):
        config = self.tasks_config['tasks'][task_key]
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=getattr(self, config['agent'])(),
            tools=[getattr(self, tool)() for tool in config.get('tools', [])]
        )

    @task
    def research_meta(self): return self._create_task('research_meta')
    @task
    def research_apple(self): return self._create_task('research_apple')
    @task
    def research_amazon(self): return self._create_task('research_amazon')
    @task
    def research_netflix(self): return self._create_task('research_netflix')
    @task
    def research_google(self): return self._create_task('research_google')
    @task
    def analysis_task(self): return self._create_task('analysis_task')

    @task
    def reporting_task(self) -> Task:
        config = self.tasks_config['tasks']['reporting_task']
        package_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(package_dir, config['output_file'])
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        def task_callback(task_output):
            return reporting_task_callback(task_output, output_file)

        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=getattr(self, config['agent'])(),
            tools=[getattr(self, tool)() for tool in config.get('tools', [])],
            callback=task_callback
        )

    # === CREW ===
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.researcher(),
                self.analyst(),
                self.reporting_analyst()
            ],
            tasks=[
                self.research_meta(),
                self.research_apple(),
                self.research_amazon(),
                self.research_netflix(),
                self.research_google(),
                self.analysis_task(),
                self.reporting_task()
            ],
            process=Process.sequential,
            verbose=True
        )
