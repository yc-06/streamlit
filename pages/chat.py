import streamlit as st

client = st.session_state.get('openai_client', None)

if client is None:
    st.warning("메인 페이지에서 API Key를 입력하세요.")
    if st.button("API Key 입력 페이지로 이동"):
        st.switch_page("st_app.py")
    st.stop()

if st.button("Clear"):
    if "messages" in st.session_state:
        del st.session_state["messages"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("대화를 입력하세요"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.responses.create(
        model="gpt-5-mini",
        input=st.session_state.messages
    )

    answer = response.output_text

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })