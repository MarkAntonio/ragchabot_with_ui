import streamlit as st



# Titulo do aplicativo

st.title('UFRPE Chatbot')


# pra rodar digite (estando no diretório do app.py):
#  streamlit run app.py

manual_aluno_page = st.Page("pages/manual_aluno.py", title="Create entry", icon=":material/add_circle:")
other_page = st.Page("pages/other_one.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([manual_aluno_page, other_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
