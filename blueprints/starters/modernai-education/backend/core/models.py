import yaml
import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq

class Models:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Models, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Loading environment variables...")
            load_dotenv("config/.env")
            with open("config/config.yaml", "r") as f:
                self.config = yaml.safe_load(f)
            self.embeddings_model = AzureOpenAIEmbeddings(
                azure_endpoint=self.config["models"]["azure_openai"]["mini_embedding_endpoint"],       
                api_key=os.getenv('AZURE_EMBEDDING_API_KEY'),
                api_version="2023-05-15"
            )
            self.setup_azure_llm()
            self.setup_groq_llm()
            self.setup_groq_fast_llm()
            self._initialized = True

    def setup_azure_llm(self):
        self.azure_llm = AzureChatOpenAI(
            azure_endpoint=self.config["models"]["azure_openai"]["endpoint-large-llm"],
            api_key=os.getenv('AZURE_GENERATION_API_KEY'),
            api_version=self.config["models"]["azure_openai"]["api_version"],
            temperature=self.config["models"]["azure_openai"]["temperature"],
            top_p=self.config["models"]["azure_openai"]["top_p"],
            frequency_penalty=self.config["models"]["azure_openai"]["frequency_penalty"],
            presence_penalty=self.config["models"]["azure_openai"]["presence_penalty"],
            max_tokens=self.config["models"]["azure_openai"]["max_tokens"]
        )
    
    def setup_groq_llm(self):
        self.groq_llm = ChatGroq(
            model=self.config["models"]["groq"]["model"],
            temperature=self.config["models"]["groq"]["temperature"], 
            max_tokens=self.config["models"]["groq"]["max_completion_tokens"],
        )

    def setup_groq_fast_llm(self):
        self.groq_fast_llm = ChatGroq(
            model=self.config["models"]["groq_fast"]["model"],
            temperature=self.config["models"]["groq_fast"]["temperature"], 
            max_tokens=self.config["models"]["groq_fast"]["max_completion_tokens"],
        )
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("config/.env")
    models = Models()

    print(models.azure_llm.invoke("Hello, world!").content)
    print(models.groq_llm.invoke("Hello, world!").content)
    print(models.groq_fast_llm.invoke("Write a short story about a cat!").content)