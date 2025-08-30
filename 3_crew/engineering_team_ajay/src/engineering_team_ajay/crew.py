from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
import os



@CrewBase
class EngineeringTeamAjay():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    """def __init__(self):
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        with open(os.path.join(config_dir, 'agents.yaml'), 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(os.path.join(config_dir, 'tasks.yaml'), 'r') as f:
            self.tasks_config = yaml.safe_load(f)"""

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )   

    @agent
    def ui_validation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_validation_engineer'],
            verbose=True,
        )

    @task
    def ui_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['ui_validation_task'],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

