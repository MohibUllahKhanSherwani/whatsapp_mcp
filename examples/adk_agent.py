import asyncio
import os
import uuid
from pathlib import Path
from examples.mcp_bridge import mcp_health_check, mcp_send_text
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.genai.types import Content, Part


load_dotenv()

APP_NAME = os.getenv("APP_NAME", "whatsapp_mcp_adk_example")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

DEFAULT_RECIPIENT_NUMBER = "+923315467120"
DEFAULT_OUTGOING_MESSAGE = "Hello from the ADK WhatsApp MCP example."

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "adk_sessions.db"
SESSION_DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

session_service = DatabaseSessionService(db_url=SESSION_DB_URL)
artifact_service = InMemoryArtifactService()


async def ensure_session(user_id: str, session_id: str, session_service, app_name: str):
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        session = await session_service.create_session(
            session_id=session_id,
            user_id=user_id,
            app_name=app_name,
        )
    return session


def initialize_agent(model: str = MODEL_NAME) -> LlmAgent:
    return LlmAgent(
        name="WhatsAppMCPAgent",
        model=model,
        static_instruction=(
            "You can call tools to check MCP health or send WhatsApp text."
        ),
        tools=[mcp_health_check, mcp_send_text],
    )


def initialize_runner(agent: LlmAgent) -> Runner:
    return Runner(
        session_service=session_service,
        artifact_service=artifact_service,
        agent=agent,
        app_name=APP_NAME,
    )


async def chat_once(
    message: str,
    user_id: str,
    session_id: str,
) -> str:
    agent = initialize_agent()
    runner = initialize_runner(agent)

    await ensure_session(
        user_id=user_id,
        session_id=session_id,
        session_service=session_service,
        app_name=APP_NAME,
    )

    content = Content(role="user", parts=[Part(text=message)])
    final_text = None
    tool_output = None

    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content:
            parts = event.content.parts or []
            for part in parts:
                text = getattr(part, "text", None)
                if text and not getattr(part, "thought", False):
                    final_text = text
                function_response = getattr(part, "function_response", None)
                if function_response is not None:
                    tool_output = str(function_response)

    if tool_output:
        return f"Tool output: {tool_output}"

    if not final_text:
        final_text = "No text response returned by model (tool call likely executed)."

    return final_text


def main() -> None:
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    prompt = (
        f"Use tool send message to send a message to {DEFAULT_RECIPIENT_NUMBER}. "
        f"The message is {DEFAULT_OUTGOING_MESSAGE}."
    )
    result = asyncio.run(chat_once(prompt, user_id=user_id, session_id=session_id))
    print(result)

if __name__ == "__main__":
    main()
