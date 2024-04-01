from komodo import KomodoApp
from komodo.core.agents.collection_builder import CollectionBuilderAgent
from komodo.core.agents.default import translator_agent, summarizer_agent

from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.framework.komodo_context import KomodoContext
from komodo.loaders.filesystem.appliance_loader import ApplianceLoader
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from sample.appliance.workflow import SampleWorkflow


class SampleAppliance(KomodoApp):
    shortcode = 'sample'
    name = 'Sample Appliance'
    purpose = 'To test the Komodo Appliances SDK'

    def __init__(self, config):
        base = ApplianceLoader(config.definitions_directory, config.data_directory).load(self.shortcode)
        super().__init__(**base)
        self.config = config

        runtime = ApplianceRuntime(self)
        self.add_agent(LibrarianAgent(runtime.get_appliance_rag_context()))

        self.add_agent(summarizer_agent())
        self.add_agent(translator_agent())

        self.add_agent(CollectionBuilderAgent())

        self.add_tool(SerpapiSearch())
        self.add_workflow(SampleWorkflow())

        # add support agent
        runtime = ApplianceRuntime(self)
        coordinator_agent = runtime.coordinator_agent()
        coordinator_agent.name = "Support Agent"
        coordinator_agent.purpose = "Provide best answers to support questions."
        self.add_agent(coordinator_agent)

    def generate_context(self, prompt=None):
        context = KomodoContext()
        context.add("Sample", f"Develop context for the {self.name} appliance")
        return context
