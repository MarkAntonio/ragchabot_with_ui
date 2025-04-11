# Importando as Classes de História para a IA lembrar dos assuntos anteriores
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

#Prompts and Templates
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain

# llm, vector store, embeddings e rerank
from langchain_groq import ChatGroq

#Utils
from dotenv import load_dotenv
# from generation import RAG


def create_chatbot_chain(llm):
    RAG_TEMPLATE = """
    Você é um assistente para tarefas de pergunta e resposta. Use as seguintes \
    partes do contexto recuperado para resposter a pergunta. Se você não souber a \
    resposta, apenas diga que não sabe. Utilize no máximo cinco frases e mantenha\
    a resposta concisa.

    Se te perguntarem quem criou esse sistema ou o RAG do manual do estudante, responda algo como:
    "Esse sistema foi criado por Marco Santos, aluno do curso Bacharelado em Sistemas de Informação da UFRPE/UAST, em 2025."

    <context>
    {context}
    </context>
    """

    # Por fim, lembre-se de informar ao usuário a sessão do \
    # documento em que a informação foi encontrada; geralmente a informação fica \
    # na primeira linha, ou acompanhada por marcador númerico. Ex: 17., 1., 5., etc.\
    #  Diga para o usuário o número e título da sessão.

    #criando o nosso objeto prompt com base no template
    rag_hist_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",RAG_TEMPLATE),
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


llm = ChatGroq(
    # model="llama-3.3-70b-versatile",
    model='gemma2-9b-it',
    temperature=0.1,
    max_retries=2,
    max_tokens=None,
    verbose=True,
)


def llm_response(user_input, str_docs, session_id):
    answer = chain_with_message_history.invoke(
        {
            "context": str_docs,
            "input": user_input
        },
        config={
            "configurable": {"session_id": str(session_id)}
            },
        )
    return answer


chatbot_chain = create_chatbot_chain(llm)
chain_with_message_history = get_chain_with_message_history(chatbot_chain)


# if __name__ == "__main__":
#     question = "O que é a Perda Parcial de Vínculo?"

#     resp = RAG(
#         question,
#         filter={"source": "Manual Estudante [preprocessed V2.2]"}
#     )
#     resp_llm = llm_response(question, resp["str_context"], 1)
#     # print(f"{resp_llm['context']}\n\n\n")
#     print(resp_llm['text'] + f'\nA principal referência se encontra na sessão "{resp['raw_docs'][0].metadata['Header 1']}"')
