
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


class RespostaResponse(BaseModel):
    """Formato da resposta devolvida pela API."""
    resposta: str
    fontes: list[Fonte]


# --- Rota principal ---
@app.post("/chat", response_model=RespostaResponse)
def chat(request: PerguntaRequest):
    """
    Recebe uma pergunta e devolve a resposta gerada pela chain de RAG,
    junto com as fontes (trechos do documento) usadas para respondê-la.
    """
    pergunta = request.pergunta.strip()
 
    # --- Tratamento de erro: pergunta vazia ---
    # HTTPException(status_code=400, ...) devolve um erro "400 Bad Request",
    # que significa "o cliente mandou algo inválido". É diferente de um erro
    # 500, que significaria "o servidor quebrou por conta própria".
    if not pergunta:
        raise HTTPException(
            status_code=400,
            detail="A pergunta não pode estar vazia.",
        )