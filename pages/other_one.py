import streamlit as st
from time import sleep
from chatbot_util import RAG, llm_response


st.write("Faça uma pergunta sobre a qualquer coisa")

# if 'messages' not in st.session_state:
#     st.session_state.messages.other = []

for message in st.session_state.messages['other']:
    if message['role'] == 'System':
        st.chat_message("s").markdown(message['content'])
    elif message['role'] == 'user':
        st.chat_message(message['role']).markdown(message['content'])
    else:
        st.chat_message(message['role']).markdown(message['content']['text'])

        with st.expander("Ver fontes"):
            for doc in message['content']['source']:
                st.write(doc['page_content'])
                st.write(f"Página: {doc['page']}  |  Score: {doc['score']}")
                st.write("***")
            
           
        

# constroi o template da entrada do prompt para mostrar os prompts
prompt = st.chat_input('Enter a prompt')

def stream_data(text: str):
    for word in text.split(" "):
        yield word + " "
        sleep(0.01)



# se o usuario aperta o enter
if prompt:
    # mostra o prompt
    st.chat_message('user').markdown(prompt)
    # Guarda o prompt como state
    st.session_state.messages['other'].append({'role': 'user', 'content': prompt})
    
    session_id = 1 # apenas pra testr
    context_dict = {"disconnected_error": True}

    while context_dict["disconnected_error"]:
        context_dict = RAG(prompt,)
        if not context_dict["disconnected_error"]:
            break
        else:
            erro = "Houve um erro na conexão com o servidor. Tentando novamente..."
            st.chat_message('System').markdown(erro)
            st.session_state.messages['other'].append({'role': 'System', 'content': erro})
    
    print(context_dict)
    answer = llm_response(prompt, context_dict['str_context'], session_id)

    

    st.chat_message('assistant').write_stream(stream_data(answer['text']))
    
    
    with st.expander("Ver fontes"):
        source_docs = ""
        for doc in context_dict['raw_docs']:
            st.write(doc.page_content)
            st.write(f"Página: {int(doc.metadata['page'])}  |  Score: {doc.metadata['score']}")
            st.write("***")
    
    st.session_state.messages['other'].append({
        'role': 'assistant',
        'content': {
            'text': answer['text'],
            'source': [
                {
                    'page_content': doc.page_content,
                    'page': int(doc.metadata['page']),
                    'score': doc.metadata['score']
                } for doc in context_dict['raw_docs']
            ]
            }
        })
