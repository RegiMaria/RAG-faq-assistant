# Tutorial do projeto

## Fonte de dados

### 1. Acesse o site da Receita Federal
Vá em [gov.br/receitafederal](https://www.gov.br/pt-br) (o portal oficial). Evite qualquer outro site que ofereça o PDF. Só baixe do domínio gov.br para garantir que é a fonte oficial.
É necessário fazer login.

### 2. Procure por "Perguntas e Respostas IRPF 2026"
Use a busca do próprio site ou vá em Centrais de Conteúdo > Publicações.
O documento também é conhecido como "[Perguntão do IR](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/dirpf/p-r-irpf-2026-v1-00-2026-04-23.pdf/view)".

### 3. Baixe o PDF
Salve o arquivo. Ele deve ter centenas de páginas (745 perguntas),
então pode demorar um pouco pra baixar.

### 4. Salve dentro do projeto
Coloque o arquivo em `data/perguntas-respostas-irpf-2026.pdf` dentro do seu repositório rag-faq-assistant,
é esse arquivo que vai virar a fonte de dados de todo o pipeline RAG.

OBS: A princípio não comite este arquivo.

## Arquivo de ingestão
O primeiro arquivo que vamos escrever é o `src/ingest.py`. Esse arquivo é responsável
pela primeira etapa do seu RAG: pegar o PDF e transformá-lo em dados que possam ser pesquisados
semanticamente.

Este arquivo contém 3 funções:
- Uma para carregamento do PDF.
- Uma para dividir o documento em `chuncks`.
- Uma para gerar e salvar os embbeding.

Ao executar esse arquivo `python src/ingest.py`
Ele vai gerar a pasta `chroma_db/`

Essa pasta é o banco vetorial do nosso RAG.

Ela vai conter os dados necessários para o Chroma armazenar:

- os chunks do PDF;
- os embeddings desses chunks;
- metadados associados aos documentos;
- os índices/estruturas usados para fazer a busca vetorial.

Nossa árvore de arquivos será:
```
rag-faq-assistant/
├── data/
│   └── perguntas-respostas-irpf-2026.pdf     <- Arquivo fonte não comitado
│
├── src/
│   ├── ingest.py    <-Arquivo atual
│   ├── rag_chain.py
│   └── main.py
│
├── chroma_db/                 ← GERADO PELO ingest.py
│   ├── ...
│   └── ...
│
├── requirements.txt
└── README.md
```
E uma observação importante: como `chroma_db/` é gerado automaticamente,
normalmente a gente também coloca no `.gitignore`:

```
venv/
.venv/

data/
chroma_db/
```

**Rodando ingest.py**
Antes de rodar ingest.py,
1. Rode o requirements.txt:

`python3 -m pip install -r requirements.txt`

2.Rode `ingest.py``:

`python3 src/ingest.py`

**Guia de troubleshooting:**
Leia a Guia de Troubleshooting aqui, caso tenhma algum problema
com os modelos.


3.Após rodar ingest.py

Se tudo estiver configurado corretamente (Ollama rodando, modelos baixados,
PDF salvo em `data/`), o terminal vai mostrar algo assim:

```text
PDF carregado: 340 páginas.
Documento dividido em 1513 chunks.
Embeddings salvos em 'chroma_db/'.
Ingestão concluída!
O vector store está pronto para uso.
```

**O que aconteceu:**

1. **Loader**: o PDF foi lido e transformado em 340 `Document` (um por página).

2. **Splitter**: esses 340 documentos foram divididos em 1513 chunks menores
   (chunk_size=1000, overlap=200).

3. **Embeddings**: cada um dos 1513 chunks foi enviado pro modelo local
   `nomic-embed-text` (via Ollama) e transformado em um vetor numérico.
   Essa é a etapa que mais demora - pode levar alguns minutos, dependendo
   da sua máquina, porque roda 100% local, sem GPU dedicada.

4. **Vector store**: todos os vetores foram salvos numa pasta nova chamada
   `chroma_db/`, criada automaticamente na raiz do projeto.

**O que conferir depois que terminar:**
- [ ] A pasta `chroma_db/` apareceu no projeto (rode `ls` ou olhe no
      explorador de arquivos)
- [ ] Ela não está vazia - deve ter arquivos dentro (um banco SQLite e
      alguns arquivos binários)
- [ ] Não é preciso rodar o `ingest.py` de novo toda vez - só se você trocar
      o PDF fonte ou mudar o `chunk_size`/`chunk_overlap`

**Se demorar muito e parecer travado:** é esperado em máquinas sem GPU -
1513 chunks passando um a um pelo modelo de embeddings local leva um
tempo. Se passar de ~15-20 minutos sem nenhuma mensagem nova, aí sim vale
investigar (verifique se o Ollama ainda está respondendo com
`ollama list` em outro terminal).

**Próximo passo:** com a `chroma_db/` criada, o projeto está pronto pra
`rag_chain.py` - que é quem vai *ler* esses vetores pra responder perguntas.