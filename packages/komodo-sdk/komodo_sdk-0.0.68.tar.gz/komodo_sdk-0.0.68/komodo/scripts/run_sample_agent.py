from komodo.core.agents.sample_agent import SampleAgent
from komodo.models.framework.agent_runner import AgentRunner
from komodo.testdata.config import TestConfig

if __name__ == "__main__":
    path = TestConfig().data_dir() / "dir1"
    agent = SampleAgent(path)
    runner = AgentRunner(agent)
    response = runner.run("Call the sample tool with hello.txt file and call hello_world function.")
    print(response.text)
