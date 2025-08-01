import os
import sys
from dotenv import load_dotenv

from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_groq import ChatGroq


log = CustomLogger().get_logger(__name__)

class ModelLoader:
    def __init__(self):
        log.info("inside __init__")
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configuration loaded succesfully", config_keys = list(self.config.keys()))

    def _validate_env(self):
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k , v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing env variables", missing_vars=missing)
            raise DocumentPortalException("Missing Environment variables", sys)
        log.info("Environment Variables validated", avaialbe_keys = [k for k in self.api_keys if self.api_keys[k]])

    def load_embddings(self):
        """
        Load and return Embedding model
        """
        try:
            log.info("Loading Embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Error Loading Embedding model", error=str(e))
            raise DocumentPortalException("Failed to Load Embedding Model", sys)


    def load_llm(self):
        """
        Load and return the LLM Model
        """
        """Load LLM dynamically based on provider in config"""
        llm_block = self.config["llm"]

        log.info("Loading LLM...")
        #Default Provider or ENV Based
        provider_key = os.getenv("LLM_PROVIDER", "groq") #Default Groq

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider_key=provider_key)
            raise DocumentPortalException(f"LLM provider not in config{provider_key}", sys)

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model=model_name, temp = temperature, max_tokens = max_tokens)

        if provider == "google":
            llm = ChatGoogleGenerativeAI(
                model = model_name,
                temperature = temperature,
                max_tokens = max_tokens
            )
            return llm
        
        elif provider == "groq":
            llm = ChatGroq(
                model = model_name,
                temperature = temperature,
                max_tokens = max_tokens    
            )
            return llm

        else:
            log.error("Unsupported LLM provider", provider = provider)
            raise DocumentPortalException(f"Unsupported LLM provider {provider}", sys)

if __name__ == "__main__":
    log.info("inside main")
    loader = ModelLoader()

    #Test Embedding Model Loading
    embeddings = loader.load_embddings()
    print(f"Embedding Model Loaded : {embeddings}")

    #Test the Embedding Model Loader
    result = embeddings.embed_query("Hello how are you")
    print(f"Embedding Result : {result}")

    # test LLM Loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM Loaded : {llm}")

    #Test the Model Loader
    result = llm.invoke("Hello how are you")
    print(f"LLM Result : {result.content}")

