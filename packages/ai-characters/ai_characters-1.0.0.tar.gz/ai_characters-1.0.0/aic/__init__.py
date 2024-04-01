from google.cloud import storage
from jsonschema import validate
from typing import List, Any
from pkg_resources import resource_string, resource_exists
from crewai import Agent

import json

BUCKET_NAME="ai-characters"


class AICharacter:
    def __init__(self, version: str, roleName: str, backstory: str, tools: List[str]):
        self.version = version
        self.roleName = roleName
        self.backstory = backstory
        self.tools = tools


def load_json_resource(package: str, resource_name: str):
    try:
        # Try to access the resource as if the package is installed
        if resource_exists(package, resource_name):
            resource = resource_string(package, resource_name)
            return json.loads(resource.decode('utf-8'))
    except Exception as e:
        # The resource wasn't found using pkg_resources, likely not installed
        print(f"Error accessing the resource through pkg_resources: {e}")
        print("Assuming that this is local run")
        pass

    # Fallback to a relative path (useful during development/testing)
    relative_path = os.path.join(os.path.dirname(__file__), resource_name)
    with open(relative_path, 'r') as file:
        return json.load(file)


def load_chracter_schema() -> Any:
    """Load the JSON schema from a file."""
    return load_json_resource('aic', 'agent.schema.json')


def load_character(key: str) -> AICharacter:
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(BUCKET_NAME)
    blob_name = f"public/{key}/character.json"
    blob = bucket.blob(blob_name)
    character_json = blob.download_as_text()
    character_data = json.loads(character_json)
    backstory_blob_name = f"public/{key}/backstory.md"
    backstory_blob = bucket.blob(backstory_blob_name)
    backstory = backstory_blob.download_as_text()

    # Load the agent schema
    schema = load_chracter_schema()

    validate(instance=character_data, schema=schema)

    tools = None
    if 'tools' in character_data:
        tools = character_data['tools']
    # Create an AICharacter instance from the JSON data
    character = AICharacter(
        version=character_data['version'],
        roleName=character_data['roleName'],
        backstory=backstory,
        tools=tools
    )
    
    return character


def load_agent(character_id: str, llm, goal, verbose=True) -> Agent:
    character = load_character(character_id)
    return Agent(
        role=character.roleName,
        goal=goal,
        backstory=character.backstory,
        tools=[],
        llm=llm,
        verbose=verbose,
        allow_delegation=True
    )
