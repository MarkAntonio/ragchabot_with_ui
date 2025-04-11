# vector store, embeddings e rerank
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_core.documents import Document

#Utils
import time
import os
from copy import deepcopy
from dotenv import load_dotenv


load_dotenv()


def init_pinecone_connection():
    return Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


def _link_vector_store_index(pinecone_conn):
    pc = pinecone_conn
    # Carregamento da primeira versao do doc

    # index_name = "testing-pinecone-vectorstore-and-embeddings"

    # novo index.
    index_name = "projeto-rag-v0-2"
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    multilingual_e5_large_embed_dim = 1024

    # se o index(a base) não existir, crie
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=multilingual_e5_large_embed_dim,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    return index


def get_vector_store(index, docs=None):
    '''
    'Doc = None' if your vector store is already filled with documents
    '''
    embeddings = PineconeEmbeddings(model="multilingual-e5-large")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    return vector_store


def _format_for_rerank(docs_from_vectorstore) -> list[dict]:
    conv_docs = []
    for i in docs_from_vectorstore:
        doc = dict(i)
        doc.pop('type')
        # O key do conteúdo em texto (page_content) deve chamar-se "Text"
        doc['text'] = doc['page_content']
        doc.pop('page_content')
        conv_docs.append(doc)
    return conv_docs


def _from_rerank_to_doc(rerank_results):
    result_dicts = []
    for doc in rerank_results.data:
        doc_copy = Document(
                id=doc['document']['id'],
                page_content=doc['document']['text'],
                metadata=deepcopy(doc['document']['metadata'])
        )
        doc_copy.metadata['score'] = doc['score']
        result_dicts.append(doc_copy)

    return result_dicts


def do_rerank(user_input: str, docs_from_vectorstore, top_n=10):
    pc.inference.rerank
    rerank_results = pc.inference.rerank(
        model="bge-reranker-v2-m3",
        query=user_input,
        documents=_format_for_rerank(docs_from_vectorstore),
        top_n=top_n,
        return_documents=True,
    )
    rerank_docs = _from_rerank_to_doc(rerank_results)
    return rerank_docs


pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = _link_vector_store_index(pc)
vector_store = get_vector_store(index=index)