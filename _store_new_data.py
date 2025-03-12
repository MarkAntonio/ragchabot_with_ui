def carregar_edital_pai():
    pc = init_pinecone_conn()
    index = _link_vector_store_index(pinecone_conn=pc)
    docs = data_loader("C:/Users/marco/OneDrive/Uast/2024.2/TAIA - Tópicos Avançados em IA [Optativa]/ProjetoRAG/rag_chatbot_ui/base_docs/2.Edital 01.2024 PAI.pdf")
    
    for doc in docs:
        doc.metadata['source'] = "Edital 01.2024 PAI"
        doc.metadata['page'] = doc.metadata['page_label']
        doc.metadata.pop('page_label')
    
    splitted_docs = data_splitter(docs)
    prefix = uuid.uuid4()
    uuids = [f"{prefix}-{_}" for _ in range(len(splitted_docs))]
    
    vector_store = get_vector_store(index=index)
    vector_store.add_documents(documents=splitted_docs, ids=uuids)



if __name__ == "__main__":
    from chatbot_util.chatbot_util import (
        data_loader,
        data_splitter,
        init_pinecone_conn,
        _link_vector_store_index,
        get_vector_store
    )
    import uuid


    pc = init_pinecone_conn()
    index = _link_vector_store_index(pinecone_conn=pc)
    # docs = data_loader("C:/Users/marco/OneDrive/Uast/2024.2/TAIA - Tópicos Avançados em IA [Optativa]/ProjetoRAG/rag_chatbot_ui/base_docs/2.Edital 01.2024 PAI.pdf")
    
    for doc in docs:
        doc.metadata['source'] = "Edital 01.2024 PAI"
        doc.metadata['page'] = doc.metadata['page_label']
        doc.metadata.pop('page_label')
    
    splitted_docs = data_splitter(docs)
    prefix = uuid.uuid4()
    uuids = [f"{prefix}-{_}" for _ in range(len(splitted_docs))]
    
    vector_store = get_vector_store(index=index)
    vector_store.add_documents(documents=splitted_docs, ids=uuids)
    

