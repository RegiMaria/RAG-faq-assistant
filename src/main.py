"""
main.py - Endpoint FastAPI que expõe a chain de RAG.

Depende de: src/rag_chain.py (usa a função perguntar()) e, por extensão,
de chroma_db/ já existir (gerado pelo ingest.py).

Como rodar:
    uvicorn src.main:app --reload

Depois, acesse http://127.0.0.1:8000/docs para testar pelo Swagger -
essa página é gerada automaticamente pelo FastAPI, você não escreve nada
pra isso acontecer.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag_chain import perguntar

# --- Cria a aplicação FastAPI ---
# É esse objeto "app" que o uvicorn procura quando você roda
# `uvicorn src.main:app` (o "app" no comando é literalmente essa variável).
app = FastAPI(
    title="FAQ Inteligente com RAG — IRPF 2026",
    description="API que responde perguntas sobre o Perguntão IRPF 2026 usando RAG local (Ollama + Chroma).",
)


# --- Modelos de dados (Pydantic) ---
# Isso define o "formato" esperado do JSON que entra e do que sai.
# O FastAPI usa essas classes pra: (1) validar automaticamente,
# (2) gerar a documentação no Swagger, (3) converter pra/de JSON sozinho.

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
# O decorador @app.post("/chat") diz: "quando chegar um POST em /chat,
# rode a função logo abaixo". O nome da função (chat) pode ser qualquer um,
# não precisa bater com o nome da rota.
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

    # --- Tratamento de erro: problema ao consultar o vector store/LLM ---
    # Isso cobre, por exemplo, o chroma_db/ não existir ainda (esqueceram
    # de rodar o ingest.py) ou o Ollama estar fora do ar.
    try:
        resultado = perguntar(pergunta)
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=(
                "Não foi possível consultar o documento. Verifique se o "
                "Ollama está rodando e se o chroma_db/ foi gerado "
                f"(rode src/ingest.py). Detalhe técnico: {erro}"
            ),
        )

    return RespostaResponse(
        resposta=resultado["resposta"],
        fontes=[Fonte(**f) for f in resultado["fontes"]],
    )


# --- Rota extra opcional: health check ---
# Não estava nos critérios de aceite, mas é uma boa prática comum em APIs:
# uma rota simples pra confirmar rapidamente "a API está de pé?" sem
# precisar chamar o LLM inteiro.
@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API do rag-faq-assistant está rodando."}