from components.backend.logging.interaction_logger import log_interaction


class MemoryAudit:
    def __init__(self):
        self.events = []

    def log_audit_event(self, *, patient_id: str, action: str, details: str):
        self.events.append((patient_id, action, details))


if __name__ == "__main__":
    audit_store = MemoryAudit()
    log_interaction(
        audit_store,
        agent_type="demo",
        patient_id="123",
        interaction_type="message",
        input_data={"message": "headaches and nausea"},
        output_data={"response": "Please reach out to a professional"},
    )
    print(audit_store.events[0])
