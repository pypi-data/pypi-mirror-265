import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

from hackathon_evaluation_rag.config import SENTENCE_TRANSFORMER_EMBEDDING_MODEL


def load_evaluator(env_file_path):

    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")

    load_dotenv(env_file_path)


    embedding_function = SentenceTransformerEmbeddings(
        model_name=SENTENCE_TRANSFORMER_EMBEDDING_MODEL
    )
    
    evaluator = AzureChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        deployment_name=os.environ["DEPLOYMENT_NAME"],
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        openai_api_type=os.environ["OPENAI_API_TYPE"],
        temperature=0,
    )

    return evaluator, embedding_function
