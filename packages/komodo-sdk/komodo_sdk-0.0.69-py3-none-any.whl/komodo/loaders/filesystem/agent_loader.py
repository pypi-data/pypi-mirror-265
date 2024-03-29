import os
from pathlib import Path

import inflection
import yaml

from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_locations import KomodoLocations
from komodo.loaders.filesystem.loader_helper import load_context_from_yaml, load_dictionary_from_yaml, load_contents
from komodo.loaders.filesystem.loader_locations import LoaderLocations


class AgentLoader():
    def __init__(self, definitions_directory: Path, data_directory: Path):
        self.locations = LoaderLocations(definitions_directory)
        self.data = KomodoLocations(data_directory)

    def load(self, agent_name: str) -> dict:
        agent_folder = self.locations.agent(agent_name)
        if not agent_folder.exists():
            raise ValueError(f"Agent {agent_name} not found in {self.locations.agents()}")

        agent_file = agent_folder / "agent.yml"
        if not agent_file.exists():
            raise ValueError(f"Agent file not found for agent {agent_name}")

        definition = load_dictionary_from_yaml(agent_file)

        context = KomodoContext()
        context_file = agent_folder / "context.yml"
        if context_file.exists():
            context = load_context_from_yaml(context_file)

        dictionary = {}
        dictionary_file = agent_folder / "dictionary.yml"
        if dictionary_file.exists():
            dictionary = load_dictionary_from_yaml(dictionary_file)

        role_file = self.locations.agent(agent_name) / "role.yml"
        role = load_contents(role_file) if role_file.exists() else None

        shortcode = definition.pop('shortcode', agent_name)
        name = definition.pop('name', f'{inflection.titleize(agent_name)}')
        purpose = definition.pop('purpose', "Generated by agent loader.")
        tools = definition.pop('tools', [])
        instructions = definition.pop('instructions', None)

        if not instructions:
            instructions_file = self.locations.agent(agent_name) / "instructions.txt"
            instructions = load_contents(instructions_file) if instructions_file.exists() else None

        if not instructions:
            raise ValueError(f"Instructions not found for agent {agent_name}")

        data_folder = self.data.agent_data(agent_name)
        data = {}
        for file in data_folder.glob("**/*"):
            if file.is_file():
                data[file.stem] = load_contents(file)

        named_parameters = dict(shortcode=shortcode,
                                name=name,
                                instructions=instructions,
                                purpose=purpose,
                                tools=tools,
                                context=context,
                                dictionary=dictionary,
                                role=role,
                                data=data)

        return {**definition, **named_parameters}

    def load_agent(self, agent_name: str) -> KomodoAgent:
        agent_data = self.load(agent_name)
        return KomodoAgent(**agent_data)

    def load_all(self) -> [KomodoAgent]:
        return [self.load_agent(agent_name) for agent_name in self.locations.available_agents()]

    def setup_agent(self, agent_name: str):
        agent_folder = self.locations.agent(agent_name)
        os.makedirs(agent_folder, exist_ok=True)
        placeholder = {
            'shortcode': agent_name,
            'name': f'{inflection.titleize(agent_name)}',
            'purpose': "Generated by agent loader.",
            'instructions': 'Please provide instructions for this agent.',
            'tools': [],
        }
        with open(agent_folder / "agent.yml", 'w') as file:
            yaml.dump(placeholder, file, default_flow_style=False, sort_keys=False)

        context = {'context': [{
            'tag': 'Sample tag',
            'content': 'This is sample context.'
        }]}
        with open(agent_folder / "context.yml", 'w') as file:
            yaml.dump(context, file, default_flow_style=False, sort_keys=False)

        dictionary = {
            'k1': 'v1',
            'k2': 'v2',
        }
        with open(agent_folder / "dictionary.yml", 'w') as file:
            yaml.dump(dictionary, file, default_flow_style=False, sort_keys=False)

        instructions = "This is a sample instruction."
        with open(agent_folder / "instructions.txt", 'w') as file:
            file.write(instructions)

        role = {
            'role': {
                'name': 'sample role',
                'description': 'This is a sample role.'
            }
        }
        with open(agent_folder / "role.yml", 'w') as file:
            yaml.dump(role, file, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    from komodo.models.framework.chat_message import ChatMessage
    from komodo.config import PlatformConfig

    config = PlatformConfig()
    loader = AgentLoader(config.definitions_directory, config.data_directory)
    agents = loader.load_all()
    for agent in agents:
        print(agent.shortcode)
        print(agent.context)
        print(agent.instructions)
        messages = ChatMessage.convert_from_context(agent.context)
        print(messages)
        print(agent.role)
        print(agent.data)

    loader.setup_agent("sample_agent")
