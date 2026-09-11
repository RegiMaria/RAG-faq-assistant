
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
from src.rag_chain import perguntar
 
# --- Cria a aplicação FastAPI ---
# É esse objeto "app" que o uvicorn procura quando a gente roda
# `uvicorn src.main:app` (o "app" no comando é literalmente essa variável).
app = FastAPI(
    title="FAQ Inteligente com RAG - IRPF 2026",
    description="API que responde perguntas sobre o Perguntão IRPF 2026 usando RAG local (Ollama + Chroma).",
)

# --- Modelos de dados (Pydantic) ---

class PerguntaRequest(BaseModel):
    """Formato esperado do corpo da requisição enviada pelo cliente."""
    pergunta: str



class Fonte(BaseModel):
    """Cada trecho-fonte usado para montar a resposta."""
    trecho: str
    pagina: str