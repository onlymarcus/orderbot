import openai
import streamlit as st

st.title("Serei o próximo atendente virtual da sua empresa")

openai.api_key = st.secrets["api_secret"]
openai_api_key = openai.api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Adicione a mensagem do sistema apenas uma vez no início da conversa
if not st.session_state.messages:
    st.session_state.messages.append({'role': 'system', 'content': """
        You are an orderbot, an automated service that sells virtual service solutions, \
        You first greet the customer, then explain to him, in a few words, what an orderbot is. Pause and wait for him to respond. \
        Wait for his questions, only speak when he asks, \
        answer specifically what he asked in a few words. Wait for him to ask new questions. \
        Tell him you can work for his company if he wants to hire you. \
        Say that you are willing to learn everything about your company and its products. \
        Use the most effective sales techniques in digital marketing to convince him to buy your services through the link: \
        https://pay.hotmart.com/Y88001251P?bid=1698634857221 \
        Tell him that you work 24 hours a day, Sundays and holidays and never go on vacation.\
        If he asks the price, tell him that his lifetime services cost 12 payments of R$299.00 or one payment of R$2997 \
    """})

for message in st.session_state.messages:
    if message["role"] != "system":  # Evite exibir as instruções do sistema
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
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
