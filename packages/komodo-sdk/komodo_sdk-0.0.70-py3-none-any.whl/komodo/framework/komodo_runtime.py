import copy

from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.framework.komodo_collection import KomodoCollection
from komodo.framework.komodo_config import KomodoConfig
from komodo.framework.komodo_user import KomodoUser
from komodo.framework.komodo_workflow import KomodoWorkflow


class KomodoRuntime():
    def __init__(self, **kwargs):
        self.appliance: KomodoApp = kwargs.get("appliance")
        self.config: KomodoConfig = kwargs.get("config", self.appliance.config if self.appliance else None)
        self.agent: KomodoAgent = kwargs.get("agent")
        self.workflow: KomodoWorkflow = kwargs.get("workflow")
        self.user: KomodoUser = kwargs.get("user", KomodoUser.default())
        self.collection: KomodoCollection = kwargs.get("collection")
        self.model = kwargs.get("model", self.agent.model if self.agent else 'gpt-3.5-turbo')
        self.temperature = kwargs.get("temperature", self.agent.temperature if self.agent else 0.5)
        self.top_p = kwargs.get("top_p", self.agent.top_p if self.agent else 1.0)
        self.seed = kwargs.get("seed", self.agent.seed if self.agent else None)
        self.max_tokens = kwargs.get("max_tokens", self.agent.max_tokens if self.agent else 1000)
        self.tools_invocation_callback = None
        self.tools_response_callback = None
        self.kwargs = kwargs

        if self.collection:
            self.collection.cache = self.config.cache()
            total_size = 0
            for file in self.collection.files:
                text = self.collection.get_file_text(file)
                total_size += len(text)
                
            if total_size > 10000:
                print("Collection is large, upgrading to GPT-4")
                self.model = 'gpt-4-turbo-preview'  # auto upgrade to GPT-4 if collection is large

    def __str__(self):
        template = "From: {} To: {} Name: {} (provider: {}, model: {})"
        return template.format(self.user.email,
                               self.agent.email,
                               self.agent.name,
                               self.agent.provider,
                               self.agent.model)

    def basecopy(self):
        return KomodoRuntime(config=self.config, appliance=self.appliance, user=self.user)

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    appliance = KomodoApp.default()
    agent = KomodoAgent.default()
    runtime = KomodoRuntime(appliance=appliance, agent=agent)
    print(runtime)

    nr = copy.copy(runtime)
    nr.agent = KomodoAgent(shortcode="new_agent", name="New Agent", instructions="New instructions")
    print(nr)

    print(runtime)
