from components.backend.llm_wrapper.gemini_client import GeminiClient

if __name__ == "__main__":
    client = GeminiClient()
    print(client.generate_text("Say hello to the engineering team."))
