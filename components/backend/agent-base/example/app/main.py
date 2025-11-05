"""Demonstrates using the AgentFoundation with FastAPI."""
from fastapi import FastAPI

from components.backend.agent_base.agent_foundation import AgentFoundation
from components.backend.llm_wrapper.gemini_client import GeminiClient


class MockStore:
    def health_check(self):
        return True

    def log_audit_event(self, **kwargs):
        print("audit", kwargs)


foundation = AgentFoundation(
    knowledge_store=MockStore(),
    patient_db=MockStore(),
    agent_type="demo",
    llm_client=GeminiClient(model_name="gemini-2.0-flash"),
)
app = FastAPI()


@app.post("/triage")
async def triage(message: str):
    response = foundation.generate_response(
        foundation.build_system_prompt("Collect essential triage details."),
        patient_context={"message": message},
    )
    return foundation.format_response(response_text=response)
