"""
01 - ingest.py - Ingestão do PDF fonte para o pipeline RAG.

Fluxo:
1. Carrega o PDF (data/perguntas-respostas-irpf-2026.pdf)
2. Divide o conteúdo em chunks
3. Gera embeddings usando o modelo local do Ollama (nomic-embed-text)
4. Salva tudo no Chroma (pasta chroma_db/), pronto para ser consultado depois

Pré-requisito: Ollama rodando localmente com o modelo de embeddings baixado
    ollama pull nomic-embed-text

Como rodar:
    python src/ingest.py
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- Configurações ---
PDF_PATH = "data/perguntas-respostas-irpf-2026.pdf"
PERSIST_DIR = "chroma_db"
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
    """
    Divide o documento em pedaços menores (chunks).

    Aqui usamos um splitter genérico por tamanho de caractere — bom ponto
    de partida. Depois de abrir o PDF e ver como cada pergunta é
    formatada (ex: sempre começa com um número tipo "001 —"), vale
    considerar um split por regex que respeite cada pergunta+resposta
    como um chunk só. Isso tende a melhorar bastante o retrieval, porque
    evita cortar uma resposta no meio.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(paginas)
    print(f"Documento dividido em {len(chunks)} chunks.")
    return chunks


def gerar_e_salvar_embeddings(chunks):
    """Gera embeddings com o modelo local do Ollama e persiste no Chroma."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    print(f"Embeddings salvos em '{PERSIST_DIR}/'.")
    return vectorstore


def main():
    paginas = carregar_documento(PDF_PATH)
    chunks = dividir_em_chunks(paginas)
    gerar_e_salvar_embeddings(chunks)
    print("Ingestão concluída! O vector store está pronto para uso.")


if __name__ == "__main__":
    main()