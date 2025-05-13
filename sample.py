import os
import yaml
import json

class SummationAgent:
    def __init__(self, env_name, business_division, ...):  # include other parameters
        self.env_name = env_name.lower()
        self.business_division = business_division.lower()

        self.load_config_and_prompts()

        self.table_name = self.config["commentary_summation"]["table_name"]
        self.columns = self.config["commentary_summation"]["columns"]
        self.output_table = self.config["commentary_summation"]["output_table"]
        self.prompt_template = self.prompts.get(f"{self.business_division.upper()}_summation_prompt")

        # Continue with any other init logic (LLM, engine, etc.)

    def load_config_and_prompts(self):
        # Go two levels up from summation_agent.py to reach project_root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        config_base_path = os.path.join(
            project_root, "configs", self.env_name, self.business_division
        )
        config_path = os.path.join(config_base_path, "config.yaml")
        prompts_path = os.path.join(config_base_path, "prompts.json")

        # Load YAML config
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Load JSON prompts
        with open(prompts_path, "r") as f:
            self.prompts = json.load(f)
