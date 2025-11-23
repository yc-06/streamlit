import streamlit as st
import base64
from openai import OpenAI

st.write("OpenAI API Key 입력")

api_key = st.text_input("OpenAI API Key 입력", type="password")

user_question = st.text_input("질문 입력")

if st.button("실행"):

    if not api_key:
        st.error("API Key 입력")
    elif not user_question:
        st.error("질문 입력")
    else:
        try:
            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "system", "content": "친절하게 답변해줘."},
                    {"role": "user", "content": user_question}
                ]
            )

            answer = response.choices[0].message.content

            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=user_question)
            image_bytes = base64.b64decode(img.data[0].b64_json)
            st.image(image_bytes)

            st.success("GPT-5-mini의 답변:")
            st.write(answer)

        except Exception as e:
            st.error(f"오류 발생: {e}")
