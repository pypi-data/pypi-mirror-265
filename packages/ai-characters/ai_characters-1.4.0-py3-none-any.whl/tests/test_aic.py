import unittest
from aic import load_character, AICharacter, _load_agent_tools

class TestDownloadAndValidateCharacterLive(unittest.TestCase):
    def test_live_deserialization(self):
        key = "jess"

        # Call the function with the actual GCS path
        character = load_character(key)

        # Verify the type of the returned object
        # Add additional assertions based on the expected content of your JSON
        self.assertIsInstance(character, AICharacter)
        # Example assertion: check if the version field matches expected value
        self.assertEqual(character.version, "1.0")

    def test_load_agent_tools(self):
        character = AICharacter(
            version="1.0",
            roleName="jess",
            backstory="",
            tools=["DATETIME"]
        )

        tools = _load_agent_tools(character)
        self.assertEqual(len(tools), 1)

if __name__ == '__main__':
    unittest.main()

# here is how to run it:
# python -m tests.test_aic