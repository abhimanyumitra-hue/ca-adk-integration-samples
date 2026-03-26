import os
import google.auth
import datetime
from zoneinfo import ZoneInfo
import google.auth.transport.requests

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.tools.data_agent.config import DataAgentToolConfig
from google.adk.tools.data_agent.credentials import DataAgentCredentialsConfig
from google.adk.tools.data_agent.data_agent_toolset import DataAgentToolset

# 1. Setup Authentication and Environment
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = "<project-id>" ## Update your project id
os.environ["GOOGLE_CLOUD_LOCATION"] = "<location>" ## Update your location
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

application_default_credentials, _ = google.auth.default()
# --- THE FIX: Force the credentials to fetch a live access token ---
auth_request = google.auth.transport.requests.Request()
application_default_credentials.refresh(auth_request)
# -------------------------------------------------------------------

credentials_config = DataAgentCredentialsConfig(
    credentials=application_default_credentials
)

# 2. Define Data Agent Tool Configuration
tool_config = DataAgentToolConfig(
    max_query_result_rows=100,
)

# 3. Instantiate the Data Agent Toolset
da_toolset = DataAgentToolset(
    credentials_config=credentials_config,
    data_agent_tool_config=tool_config,
    tool_filter=[
        "ask_data_agent",
    ],
)

# 4. Define the Root Agent
# 4. Define the Root Agent
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-pro", 
    ),
    ## Update the data agent uri
    instruction=f"""You are a helpful AI assistant designed to provide accurate and useful information.
    Your GCP project id is: {project_id}.

    Use only the data agent with the name "<data agent uri>" 
    """,
    tools=[da_toolset],
)

# 5. Initialize the App (DO NOT call .run() here)
app = App(
    name="adk_dataagent_tool",
    root_agent=root_agent
)