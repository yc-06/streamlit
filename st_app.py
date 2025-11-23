import streamlit as st
from openai import OpenAI

st.title("간단한 응답 페이지")
st.write("OpenAI API Key 입력")

api_key = st.text_input("OpenAI API Key 입력", type="password")
user_question = st.text_input("질문 입력")

if api_key:
    st.session_state["OPENAI_API_KEY"] = api_key
    client = OpenAI(api_key=api_key)
    st.session_state["openai_client"] = client
if user_question:
    st.session_state["USER_QUESTION"] = user_question

@st.cache_data
def get_answer(api_key, user_question):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "친절하게 답변해줘."},
            {"role": "user", "content": user_question}
        ]
    )
    return response.choices[0].message.content

if st.button("실행"):

    if not api_key:
        st.error("API Key 입력")
    elif not user_question:
        st.error("질문 입력")
    else:
        try:
            answer = get_answer(api_key, user_question)

            st.success("GPT-5-mini의 답변:")
            st.write(answer)

        except Exception as e:
            st.error(f"오류 발생: {e}")