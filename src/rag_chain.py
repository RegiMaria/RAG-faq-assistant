from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Configurações ---
PERSIST_DIR = "chroma_db"
LLM_MODEL = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
TOP_K = 4

# --- Prompt template ---
# Instrui o modelo a responder SOMENTE com base no contexto recuperado,
# reduzindo o risco de alucinação.
# Este é ponto central do "problema de negócio"
# deste projeto.
PROMPT_TEMPLATE = """Você é um assistente que responde perguntas sobre o
Imposto de Renda com base EXCLUSIVAMENTE no contexto abaixo, extraído do
documento oficial "Perguntas e Respostas IRPF 2026" da Receita Federal.
 
Se a resposta não estiver no contexto, diga claramente que não encontrou
essa informação no documento. Não invente uma resposta.
 
Contexto:
{context}
 
Pergunta: {question}
 
Resposta:"""