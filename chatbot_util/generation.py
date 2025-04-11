# Importando as Classes de História para a IA lembrar dos assuntos anteriores
from .retrieve import (
    vector_store, 
    do_rerank
)

#Utils
from dotenv import load_dotenv


load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) if docs else "No documents found"


def _drop_low_score_docs(docs):
    return [doc for doc in docs if doc.metadata['score'] > 0.5]


def RAG(user_input, filter:dict=None) -> str:
    try:
        docs_vectorstore = vector_store.similarity_search(user_input, k=12, filter=filter)
        # para esse documento do manual do aluno, apenas 6 docs já são o suficiente
        docs_rerankeds = do_rerank(user_input, docs_vectorstore, top_n=6)
        top_docs_rerankeds = _drop_low_score_docs(docs_rerankeds)
        return {'str_context': format_docs(top_docs_rerankeds), 'raw_docs': top_docs_rerankeds, 'disconnected_error': False}
    except Exception as remote_disconected:
        print(remote_disconected)
        return {"disconnected_error": True}

def RAG_without_reranking(user_input, filter:dict=None) -> str:
    try:
        docs_vectorstore = vector_store.similarity_search_with_relevance_scores(user_input, k=5, filter=filter)
        return docs_vectorstore
        # return {'str_context': format_docs(docs_vectorstore), 'raw_docs': docs_vectorstore, 'disconnected_error': False}
    except Exception as remote_disconected:
        print(remote_disconected)
        return {"disconnected_error": True}



# if __name__ == "__main__":
#     resp = RAG("Quais são osProgramas de Apoio aos Estudantes de Graduação?", filter={"source": "Manual Estudante [preprocessed V2.2]",})
#     print(resp)
#     for index, _ in enumerate(resp['raw_docs']):
#         print(f'=========== document {index + 1} ===========')
#         print(_)
       

''' def main_old():
  session_id = int(input("Digite o número de sua sessão: "))

  print("""Chatbot iniciado... \n
  Para finalizar a conversa digite /exit
  ou para encerrar a sessão digite /session\n """)

  while True:
      question = input("> ")
      if question == "/exit":
        break
      elif question == "/session":
        session_id = int(input("Digite o número de sua sessão: "))
        continue
      #recuperando os top3 documentos mais similares à minha pergunta (esperamos que a resposta esteja nestes documentos)
      context = RAG(question)
      answer = llm_response(question, context, session_id)
      print(answer["text"], '\n')

#main_old()
'''
