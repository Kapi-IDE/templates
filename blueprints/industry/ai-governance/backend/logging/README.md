# Interaction Logger

Single function helper that records agent interactions into a patient database audit log while emitting best-effort telemetry on failure.

## Usage
```python
from components.backend.logging.interaction_logger import log_interaction

log_interaction(
    patient_db,
    agent_type="triage",
    patient_id="123",
    interaction_type="message",
    input_data={"message": "I feel dizzy"},
    output_data={"response": "Please consider speaking to a doctor"},
)
```

Run `example/log_usage.py` to see the helper writing to an in-memory audit store.
