import streamlit as st
import traceback

# Titulo do aplicativo
if __name__ == '__main__':
    st.title('UFRPE Chatbot')

    # pra rodar digite (estando no diretório do app.py):
    #  streamlit run app.py

    manual_aluno_page = st.Page("pages/manual_aluno.py", title="Manual do Aluno", icon=":material/chat:")
    # other_page = st.Page("pages/edital_pai.py", title="Edital Pai 2024.1", icon=":material/chat:")

    # pg = st.navigation([manual_aluno_page, other_page])
    pg = st.navigation([manual_aluno_page])

    # if 'messages' not in st.session_state:
    #     st.session_state.messages = {
    #         "manual_aluno": [],
    #         "edital_pai": []
    #         }

    if 'messages' not in st.session_state:
        st.session_state.messages = {
            "manual_aluno": []
            }
    # st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
    try:
        pg.run()
    except Exception:
        traceback.print_exc()
        st.error("Ocorreu um erro com a plataforma, tente novamente mais tarde.")
