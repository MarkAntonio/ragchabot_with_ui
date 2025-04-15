import streamlit as st

# Titulo do aplicativo

st.set_page_config(page_title="UFRPE Chatbot", page_icon=":material/edit:")
st.title('UFRPE Chatbot')

if __name__ == "__main__":
    from PIL import Image
    from chatbot_util.chabot import set_model, set_temperature
    from pages.manual_aluno import clear_history

        
    # pra rodar digite (estando no diretório do app.py):
    #  streamlit run app.py
    st.sidebar.image(Image.open("assets/UAST - UFRPE logo.png"))

    with st.sidebar:
        option = st.selectbox(
            "Modelo da LLM",
            ("gemma2-9b-it", "llama-3.3-70b-versatile", "qwen-qwq-32b"),
        )
        set_model(option)   
        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=2.0,
            step=0.01,
            format="%0f"
        )
        set_temperature(temperature)

        if st.button("Apagar Histórico", type="primary", icon=":material/delete:"):
            clear_history()
        st.page_link("https://drive.google.com/file/d/11IZBFp3QkrNhNa9chBCfX6juFdSMkPis/view?usp=sharing", label="Documento original", icon=":material/open_in_new:")


    manual_aluno_page = st.Page("pages/manual_aluno.py", title="Create entry", icon=":material/add_circle:")
    # other_page = st.Page("pages/other_one.py", title="Delete entry", icon=":material/delete:")

    pg = st.navigation([manual_aluno_page])
    # st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
    pg.run()
