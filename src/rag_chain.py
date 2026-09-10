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


def montar_retriever():
    """Conecta no vector store já populado e retorna um retriever."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K})


def formatar_contexto(documentos):
    """Junta os chunks recuperados em um único bloco de texto para o prompt."""
    return "\n\n---\n\n".join(doc.page_content for doc in documentos)

def montar_chain():
    """Monta a chain completa: retriever -> prompt -> LLM -> texto."""
    retriever = montar_retriever()
    llm = ChatOllama(model=LLM_MODEL, temperature=0) # Temperatura é uma configuração para deixar a geração mais determinística.
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
 
    chain = (
        {
            "context": retriever | formatar_contexto,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


 
def perguntar(pergunta: str) -> dict:
    """
    Função principal: recebe uma pergunta e devolve a resposta junto
    com os trechos-fonte usados (para você conseguir verificar/citar).
    """
    chain, retriever = montar_chain()
 
    resposta = chain.invoke(pergunta)
    fontes = retriever.invoke(pergunta)
 
    return {
        "resposta": resposta,
        "fontes": [
            {
                "trecho": doc.page_content[:200] + "...",
                "pagina": doc.metadata.get("page", "desconhecida"),
            }
            for doc in fontes
        ],
    }
 
 
if __name__ == "__main__":
    pergunta = "Preciso declarar se recebi um imóvel de herança?"
    resultado = perguntar(pergunta)
    print("Resposta:", resultado["resposta"])
    print("\nFontes usadas:")
    for f in resultado["fontes"]:
        print(f"- (página {f['pagina']}) {f['trecho']}")
 
 