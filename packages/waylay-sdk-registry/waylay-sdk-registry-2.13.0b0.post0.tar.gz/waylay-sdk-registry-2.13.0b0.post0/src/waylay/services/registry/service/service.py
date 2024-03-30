"""Registry Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.default_api import DefaultApi
from ..api.jobs_api import JobsApi
from ..api.models_api import ModelsApi
from ..api.plugs_api import PlugsApi
from ..api.runtimes_api import RuntimesApi
from ..api.schemas_api import SchemasApi
from ..api.webscripts_api import WebscriptsApi


class RegistryService(WaylayService):
    """Registry Service Class."""

    name = "registry"
    title = "Registry Service"

    jobs: JobsApi
    models: ModelsApi
    plugs: PlugsApi
    runtimes: RuntimesApi
    schemas: SchemasApi
    webscripts: WebscriptsApi
    default: DefaultApi

    def __init__(self, api_client: ApiClient):
        """Create the registry service."""

        super().__init__(api_client)
        self.jobs = JobsApi(api_client)
        self.models = ModelsApi(api_client)
        self.plugs = PlugsApi(api_client)
        self.runtimes = RuntimesApi(api_client)
        self.schemas = SchemasApi(api_client)
        self.webscripts = WebscriptsApi(api_client)
        self.default = DefaultApi(api_client)
