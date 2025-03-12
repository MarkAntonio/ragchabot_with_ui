"""Basedo no artigo: https://medium.com/@pani.chinmaya/memory-for-your-rag-based-chat-bot-using-langchain-b4d720031671
"""
# python -m pip install -U langchain-pinecone pinecone-notebooks langchain_community langchain-huggingface python-dotenv pypdf langchain_groq streamlit

# Commented out IPython magic to ensure Python compatibility.

# %pip install -qU langchain-pinecone pinecone-notebooks
# %pip install -qU langchain_community
# %pip install -qU langchain-huggingface
# %pip install -qU python-dotenv
# %pip install -qU pypdf
# %pip install -U langchain_groq
# installing a Lib for creating GUI
# %pip install streamlit


# load docs

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Importando as Classes de História para a IA lembrar dos assuntos anteriores
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain

# llm, vector store, embeddings e rerank
from langchain_groq import ChatGroq
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_core.documents import Document

#Utils
import time
import os
from copy import deepcopy
from dotenv import load_dotenv



#Prompts and Templates



# Commented out IPython magic to ensure Python compatibility.
# %pip install docling-core[chunking]


# Não vou usar agora pois vou usar a API do Pinecone
def data_loader(path):
    pdf_loader = PyPDFLoader(path)
    documents = pdf_loader.load()
    return documents


# não vou usar agora, vou usar a API do pinecone que já está com os daddos
def data_splitter(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    return docs


def init_pinecone_conn():
    return Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


def _link_vector_store_index(pinecone_conn):
    pc = pinecone_conn
    index_name = "testing-pinecone-vectorstore-and-embeddings"  # change if desired
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


def create_chatbot_chain(llm):
    RAG_TEMPLATE = """
    Você é um assistente para tarefas de pergunta e resposta. Use as seguintes \
    partes do contexto recuperado para responder a pergunta. Se você não souber a \
    resposta, apenas diga que não sabe. Utilize no máximo cinco frases e mantenha\
    a resposta concisa.

    <context>
    {context}
    </context>
    """

    #criando o nosso objeto prompt com base no template
    rag_hist_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RAG_TEMPLATE),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    #criando a chain recebendo o prompt e o modelo
    return LLMChain(prompt=rag_hist_prompt, llm=llm)


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_chain_with_message_history(chatbot_chain):
    chain_with_message_history = RunnableWithMessageHistory(
        chatbot_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    return chain_with_message_history


load_dotenv()


pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = _link_vector_store_index(pc)
vector_store = get_vector_store(index=index)

llm = ChatGroq(
    #model="llama-3.3-70b-versatile",
    model='gemma2-9b-it',
    temperature=0.1,
    max_retries=2,
    max_tokens=None,
    verbose=True,
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) if docs else "No documents found"


def _drop_low_score_docs(docs):
    return [doc for doc in docs if doc.metadata['score'] > 0.5]


def get_docs_by_ids(ids):
    docs = []
    results = index.fetch(ids=ids)
    print(results)


def bring_complemented_docs(config, docs: list = None):
    try:
        index_and_id = []
        docs = docs[:5]
        prefix_id = "92bff8e0-5607-419e-a1b4-5c26946c4863-"
        for index, doc in enumerate(docs):
            
            index_and_id.append({
                'index': index,
                'id': doc.id,
                'score': doc.metadata['score']
                })
        
        neighbor_ids = []
        for i in index_and_id:
            suffix_id = i['id'].split(prefix_id)[1]
            if int(suffix_id) > 0:
                ids = [prefix_id + str(int(suffix_id) - 1), prefix_id + str(int(suffix_id) + 1)]
            else:
                ids = [prefix_id + str(int(suffix_id) + 1), prefix_id + str(int(suffix_id) + 2)]
            neighbor_ids.append({
            'original_index': i['index'],
            "ids": ids

        })
    
        print(neighbor_ids)
        pc_index = _link_vector_store_index(pc)
        rec_data = pc_index.fetch(neighbor_ids[0]['ids'])
        print(rec_data)
    
    except Exception as e:
        print(e)


def RAG(user_input, filter: dict = None) -> str:

    try:
        docs_vectorstore = vector_store.similarity_search(user_input, k=20, filter=filter)
        docs_rerankeds = do_rerank(user_input, docs_vectorstore)
        # docs_reranked_complemented = bring_complemented_docs("edital_pai", docs=docs_rerankeds)
        return {'str_context': format_docs(docs_rerankeds), 'raw_docs': docs_rerankeds, 'disconnected_error': False}
    except Exception as remote_disconected:
        print(remote_disconected)
        return {"disconnected_error": True}


chatbot_chain = create_chatbot_chain(llm)
chain_with_message_history = get_chain_with_message_history(chatbot_chain)


def llm_response(user_input, str_docs, session_id):
    answer = chain_with_message_history.invoke({
        "context": str_docs,
        "input": user_input
    },
    config={
        "configurable": {"session_id": str(session_id)}
        },
    )
    return answer
