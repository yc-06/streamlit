import streamlit as st
from openai import OpenAI

st.header("PDF 챗봇")

client = st.session_state.get("openai_client", None)
if client is None:
    st.warning("API Key가 필요합니다. 메인 페이지에서 입력하세요.")
    st.stop()

pdf_file = st.file_uploader("PDF 파일 업로드", type=['pdf'])
if pdf_file:
    if 'vector_store' not in st.session_state:
        vector_store = client.vector_stores.create(name="ChatPDF")
        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=[pdf_file]
        )
        st.session_state.vector_store = vector_store
        st.success("PDF 업로드 완료")

if 'vector_store' not in st.session_state:
    st.info("PDF 파일을 업로드해야 챗봇 사용이 가능합니다.")
    st.stop()

if "pdf_chat_messages" not in st.session_state:
    st.session_state.pdf_chat_messages = [
        {"role":"system","content":"""
당신은 PDF 문서 내용을 안내하는 챗봇입니다.
PDF 내용을 바탕으로 질문에 답하고, 내용에 없으면 모른다고 답하세요.
"""}
    ]

if st.button("Clear"):
    st.session_state.pdf_chat_messages = [
        {"role":"system","content":"""
당신은 PDF 문서 내용을 안내하는 챗봇입니다.
PDF 내용을 바탕으로 질문에 답하고, 내용에 없으면 모른다고 답하세요.
"""}
    ]

for msg in st.session_state.pdf_chat_messages[1:]:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])

if user_input := st.chat_input("PDF 관련 질문 입력"):
    user_msg = {"role":"user", "content":user_input}
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.pdf_chat_messages.append(user_msg)

    response = client.responses.create(
        model="gpt-5-mini",
        input=st.session_state.pdf_chat_messages,
        tools=[{
            "type":"file_search",
            "vector_store_ids":[st.session_state.vector_store.id]
        }]
    )
    assistant_msg = {"role":"assistant", "content":response.output_text}
    with st.chat_message("assistant"):
        st.markdown(assistant_msg["content"])
    st.session_state.pdf_chat_messages.append(assistant_msg)