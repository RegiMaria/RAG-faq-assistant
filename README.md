<div align="center"> <img width="1584" height="396" alt="Banner rag-faq-assistant" src="https://github.com/user-attachments/assets/65605a1b-fcfb-46ec-accd-e4fa2e6a3604" /> </div>


# FAQ Inteligente com RAG 

Assistente que responde perguntas sobre um documento próprio (ex: FAQ do Imposto de Renda) usando RAG (Retrieval-Augmented Generation),
100% com ferramentas locais e gratuitas.

## O que vamos aprender
 Conceitos de RAG na prática, como funciona embeddings/similaridade, estrutura básica de uma API REST, uso introdutório do LangChain.

 ## Objetivo
  Aprender os fundamentos de IA generativa e RAG construindo um chatbot que responde perguntas sobre documentos próprios (ex: manual de um produto, PDF de políticas internas).

## O problema: busca manual em documentos longos
Busca manual em docuemntos loongos é lenta, 
sujeita a erro (a pessoa não sabe o termo técnico certo pra usar no Ctrl+F)
e depende de conhecimento prévio de onde a resposta está.
Isso gera retrabalho, dúvidas não resolvidas.

## A solução que o RAG resolve: 
Em vez da pessoa procurar a informação, ela pergunta em linguagem natural e o
sistema busca o trecho certo entre as 745 perguntas (retrieval) e formula a resposta com base
apenas no conteúdo oficial (generation).

## Justificativa:

RAG ancora a resposta no documento oficial.
Reduzindo o risco de alucinação que um LLM sozinho teria ao "chutar" uma resposta sobre o documento.

### Stack:
- Python + FastAPI (endpoint /chat)
- LangChain (loaders, text splitters, chain de RAG)
- Embeddings (OpenAI ou modelo open-source via HuggingFace - a definir)
- Vector DB local (Chroma)

**Este é o projeto 1 de 3 para aprender sobre RAG.⭐**

**Referências:**
- [RAG - para baixinhos](https://lnkd.in/p/d3YQS3CZ)
- [RAG - Introdução](https://lnkd.in/p/dNHGhfpH)


Vem conhecer a comunidade Tech feminina: FirstCommit-m
<div align="center"> <img width="200" alt="FirstCommit Mulher" src="https://github.com/user-attachments/assets/549b041a-c598-4c2e-bf9f-b47be6ad78ae" />

<a href="https://www.instagram.com/firstcommitmulher/"> <img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white" alt="Instagram"/> </a> </div>
 
