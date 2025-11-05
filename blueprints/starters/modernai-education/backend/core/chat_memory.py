import json
import time

class ChatMemory:
    def __init__(self, id: str):
        self.id = id
        self.memory = []
        self.file_name = f'db/chat_memory_{self.id}.json'

    def load_memory(self):
        try:
            with open(self.file_name, 'r') as f:
                self.memory = json.loads(f.read())
        except FileNotFoundError:
            self.memory = []
            self.save_memory()

    def save_memory(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def add_to_memory(self, query: str, response: str):
        self.memory.append({
            "timestamp": time.time(),
            "query": query,
            "response": response
        })
        self.save_memory()

    def get_all_messages(self):
        return self.memory
    
    def get_last_few_messages_string(self, num_messages: int = 5):
        return "\n".join([f"{item['timestamp']}: {item['query']} -> {item['response']}" for item in self.memory[-num_messages:]])
    
    def get_memory_string(self):
        return "\n".join([f"{item['timestamp']}: {item['query']} -> {item['response']}" for item in self.memory])
