import os
import yaml
import json

class SummationAgent:
    def __init__(self, env_name, business_division, ...):  # Add other existing params
        self.env_name = env_name
        self.business_division = business_division.lower()  # e.g., "gf"
        
        self.load_config_and_prompts()

        # Use these loaded configs
        self.table_name = self.config["commentary_summation"]["table_name"]
        self.columns = self.config["commentary_summation"]["columns"]
        self.output_table = self.config["commentary_summation"]["output_table"]
        self.prompt_template = self.prompts.get(f"{business_division.upper()}_summation_prompt")

        ...
        # (rest of init logic continues)

    def load_config_and_prompts(self):
        # Path to the env + business division folder
        base_path = os.path.join(self.env_name, self.business_division)

        config_path = os.path.join(base_path, "config.yaml")
        prompts_path = os.path.join(base_path, "prompts.json")

        # Load YAML config
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Load JSON prompts
        with open(prompts_path, "r") as f:
            self.prompts = json.load(f)
