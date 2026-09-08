# RAG-faq-assistante

## Pipeline RAG

O pipeline RAG tem fases bem distintas:
**Indexação** e **Consulta**



![alt text](https://github.com/RegiMaria/RAG-faq-assistant/blob/docs/tutorial/docs/images/image.png)


![alt text](https://github.com/RegiMaria/RAG-faq-assistant/blob/docs/tutorial/docs/images/image-1.png)

## O que cada componente faz

**Fase de indexação (roda uma vez)**

**1.Loader:** lê o arquivo fonte (PDF, TXT, site) e transforma em texto que o código consegue manipular.

**2.Splitter (chunking):** quebra o texto grande em pedaços menores, porque o modelo não consegue (e não deveria) processar o documento inteiro de uma vez.

**3.Embeddings:** transforma cada chunk de texto em um vetor numérico que representa seu "significado" - textos com sentido parecido geram vetores próximos entre si.

**4.Vector store:** banco que guarda esses vetores de forma que dê pra buscar por similaridade rapidamente (no nosso caso, o Chroma).

**5.Fase de consulta (roda a cada pergunta):**

**6.Retriever:** pega a pergunta do usuário, transforma ela também em vetor, e busca no vector store os chunks mais parecidos (é aqui que a "R" de Retrieval acontece).

**7.Prompt template:** monta a mensagem final que vai pro LLM, juntando a pergunta original + os chunks recuperados como contexto - geralmente com uma instrução tipo "responda só com base no contexto abaixo".

**9.LLM:** lê esse prompt e gera a resposta em linguagem natural (é aqui que a "G" de Generation acontece).

Resposta + fontes: idealmente você retorna não só o texto, mas também de quais chunks/páginas ele tirou a informação - isso é o que dá confiança pra resposta.

**10.LangSmith:** Uma camada de avaliação/observabilidade - sem isso você não sabe se o sistema está funcionando bem ou só "parecendo" funcionar.

## Bibliotecas Python