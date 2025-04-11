def carregar_manual_estudante_markdown():
    pc = init_pinecone_connection()
    index = _link_vector_store_index(pinecone_conn=pc)
    docs = data_loader("C:/Users/marco/OneDrive/Uast/2024.2/TAIA - Tópicos Avançados em IA [Optativa]/ProjetoRAG/rag_chatbot_ui/docs/preprocessed_docs/manual_do_estudante.md")
    
    
    splitted_docs = data_splitter_manual_aluno(docs)
    uuids = [str(uuid.uuid4()) for _ in range(len(splitted_docs))]
    
    vector_store = get_vector_store(index=index)
    vector_store.add_documents(documents=splitted_docs, ids=uuids)
    print("Documentos carregados com sucesso!")

def delete_all():
    pc = init_pinecone_connection()
    index = _link_vector_store_index(pinecone_conn=pc)
    index.delete(delete_all=True)
    print("Todos os documentos deletados com sucesso!")


# if __name__ == "__main__":
#     from indexing import (
#         data_loader,
#         data_splitter_manual_aluno)
#     from retrieve import (
#         init_pinecone_connection,
#         _link_vector_store_index,
#         get_vector_store
#     )
#     import uuid


#     pc = init_pinecone_connection()
#     index = _link_vector_store_index(pinecone_conn=pc)
    
#     carregar_manual_estudante_markdown()

    ### delete_all()