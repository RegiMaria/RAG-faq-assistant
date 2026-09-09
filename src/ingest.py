import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ----Configurações----

PDF_PATH = "data/perguntas-respostas-irpf-2026.pdf"
PERSIST_DIRECTORY = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def carregar_documento(caminho: str):
    """Carrega o PDF e retorna uma lista de Documents (um por página)."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"PDF não encontrado em '{caminho}'. Baixe o Perguntão IRPF 2026 "
            "no site oficial da Receita Federal e salve nesse caminho."
        )
    loader = PyPDFLoader(caminho)
    paginas = loader.load()
    print(f"PDF carregado: {len(paginas)} páginas.")
    return paginas


 
def dividir_em_chunks(paginas):
    """Divide o documento em chunks menores para facilitar a busca semântica."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(paginas)
    print(f"Documento dividido em {len(chunks)} chunks.")
    return chunks



