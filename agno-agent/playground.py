import os
from agno.agent import Agent
from agno.models.litellm.litellm_openai import LiteLLMOpenAI
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.playground import PlaygroundSettings

agent_storage: str = "tmp/agents.db"

# Fetch ENV variables
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-xxxxxx")


litellm_model = LiteLLMOpenAI(
    id="openrouter/anthropic/claude-3-5-haiku-20241022",
    base_url="http://litellm.local.oderna.in/",
    api_key=LITELLM_API_KEY,
)

web_agent = Agent(
    name="Web Agent",
    model=litellm_model,
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    # Adds the current date and time to the instructions
    add_datetime_to_instructions=True,
    # Adds the history of the conversation to the messages
    add_history_to_messages=True,
    # Number of history responses to add to the messages
    num_history_responses=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=litellm_model,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)
playground = Playground(
    agents=[web_agent, finance_agent],
    settings=PlaygroundSettings(cors_origin_list=["http://192.168.31.222:3000"])
)
app = playground.get_app()

if __name__ == "__main__":
    playground.serve("playground:app", reload=True, port=8000, host="0.0.0.0")
