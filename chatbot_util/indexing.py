# load docs
from langchain.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, TokenTextSplitter


# Uso apenas uma vez para carregar a vectorstore do pinecone
def data_loader(path):
    with open(path, 'r', encoding="utf-8") as arquivo:
        doc = arquivo.read()
    return doc


# Uso apenas uma vez para tratar o manual do aluno
def data_splitter_manual_aluno(manual_aluno):  
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        # ("-", "Section"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    manual_splits = markdown_splitter.split_text(manual_aluno)

    del manual_splits[:10] #deletando do início ao sumário para evitar dados duplicados
    del manual_splits[41:] # deletando tabelas finais que não tenho uso no momento

    t_text_splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=50)
    manual_t_splits = t_text_splitter.split_documents(manual_splits)

    # inserindo cabeçalho no texto para encontrar mais fácil
    for section in manual_t_splits:
        headers = ""
        if section.metadata.get('Header 1'):
            headers += f"{section.metadata['Header 1']}\n"
        if section.metadata.get('Header 2'):
            headers += f"{section.metadata['Header 2']}\n"
        if section.metadata.get('Header 3'):
            headers += f"{section.metadata['Header 3']}\n"
        # if section.metadata.get('Section'):
        #     headers += f"{section.metadata['Section']}\n"
        section.page_content = f"{headers}{section.page_content}"

    # inserido metadata id
    for idx, text in enumerate(manual_t_splits):
        text.metadata["chunk_id"] = idx
        text.metadata['source'] = "Manual Estudante [preprocessed V2.2]"
   
    return manual_t_splits

# if __name__ == "__main__":
#     doc = data_loader("C:/Users/marco/OneDrive/Uast/2024.2/TAIA - Tópicos Avançados em IA [Optativa]/ProjetoRAG/rag_chatbot_ui/docs/preprocessed_docs/manual_do_estudante.md")

#     splits = data_splitter_manual_aluno(doc)

#     for i in splits:
#         print(i)
