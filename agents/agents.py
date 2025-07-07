import os
import asyncio
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.genai import types # For creating message Content/Parts
from src.prompts import SDS_AGENT_INSTRUCTION

# --- Hazmat SDS Agent Setup ---
def create_sds_search_agent(model='gemini-2.5-flash'):
    agent = Agent(
        name="HazmatSDSFinder",
        model=model,
        description="Agent to search for official SDS/FISPQ and return relevant safety information for a product.",
        instruction=SDS_AGENT_INSTRUCTION,
        tools=[google_search]
    )
    return agent


# --- Composition Search Agent Setup ---
def create_composition_search_agent(model='gemini-2.5-flash'):
    agent = Agent(
        name="HazmatCompositionFinder",
        model=model,
        description="Agent to search for chemical composition of a product and determine if it contains hazardous materials.",
        instruction="You will receive product information and must search for its chemical composition. If the composition contains hazardous materials, return 'yes', otherwise return 'no'.",
        tools=[google_search]
    )
    return agent

# --- Query Function ---
def query_agent(agent, product_query, session_id="session_001", user_id="user_1"):
    app_name = agent.name
    session_service = InMemorySessionService()
    # Create new session for each call, for resetting context
    async def create_session():
        return await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
    asyncio.run(create_session())

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )
    
    content = types.Content(role='user', parts=[types.Part(text=product_query)])
    final_response_text = "Agent did not produce a final response."
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
    return final_response_text


