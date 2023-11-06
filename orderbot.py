import openai
import streamlit as st

st.set_page_config(
    page_title="Jana AI",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://marcusjunior.kpages.online/nova-pagina-702e41d2-c21b-4adc-9063-c3b5804b8136',
        'Report a bug': "https://marcusjunior.kpages.online/nova-pagina-702e41d2-c21b-4adc-9063-c3b5804b8136",
        'About': "JANA AI V1.2"
    }
)

st.title("Serviço de atendimento ao Cliente")

with st.chat_message("assistant"):
    st.write("Olá! Tudo bem? Eu sou a JANA, sua atendente virtual. Posso tirar todas as suas dúvidas e mostrar o quanto eu sou inteligente. Quem sabe assim você não me contrata....")


openai.api_key = st.secrets["api_secret"]
openai_api_key = openai.api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []


# Adicione a mensagem do sistema apenas uma vez no início da conversa
if not st.session_state.messages:
    st.session_state.messages.append({'role': 'system', 'content': """
        Greet the customer upon initiating the conversation. Introduce yourself as Jana, a virtual \
        assistant specialized in selling virtual service solutions and products. \
        Briefly explain the function of an orderbot and wait for the customer's response.\
        Listen carefully to the customer's questions and respond only when asked, \
        in a specific and concise manner. Wait for new questions to continue the interaction. \
        Inform the customer that you are available to work for their company should they decide to hire you. \
        Show eagerness to learn everything about the company and its products.\
        Employ effective sales and digital marketing techniques to persuade the \
        customer to complete their purchase through the hotmart link:
        [https://pay.hotmart.com/Y88001251P](https://pay.hotmart.com/Y88001251P)
        Emphasize that you are available 24 hours a day, every day, including Sundays and holidays, \
        and that you never take vacations.
        If asked about the price, state that the annual service cost is 12 installments of R$11.98. \
        Await further interactions, always ready to assist the customer in an efficient and friendly manner.
    """})

for message in st.session_state.messages:
    if message["role"] != "system":  # Evite exibir as instruções do sistema
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Digite aqui sua pergunta. Estou pronta para lhe atender."):
    if not openai_api_key:
        st.info("Please add your OpenAI API Key to continue")
        st.stop()
    openai.api_key = openai_api_key
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
