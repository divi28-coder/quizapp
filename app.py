from google import genai
import json
import streamlit as st

client = genai.Client(api_key=st.secrets("GOOGLE_API_KEY"))

st.title("AI Quiz Generator and Evaluator")

topic = st.text_input("give a topic for generating quiz questions")
if st.button("Generate Quiz"):
    prompt = f"""You are expert in generating quiz questions.
    For the following topic-{topic}, generate 5 quiz questions in the following format.
    {{"question":"text",
    "options":["A","B","C","D"],
    "correct":0,
    "explanation":"short explanation"
    }}
    dont add anything before or after this."""

    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )

    data = json.loads(response.text)
    st.session_state.quiz = data

if "quiz" in st.session_state:
    st.header("Quiz Question")
    num = 1
    for ques in st.session_state.quiz:
        st.write(str(num) + ". " + ques['question'])
        st.radio("Choose:", ques['options'], key="choosen_answer" + str(num))
        num += 1

    if st.button("Submit"):
        st.header("Results")

        st.session_state.points = 0
        numb = 1
        for j in st.session_state.quiz:
            if j['options'][j['correct']] == st.session_state['choosen_answer' + str(numb)]:
                st.session_state.points += 1
            numb += 1

        st.write(f"You have answered {st.session_state.points} questions correctly")

        st.header("Explanations")
        number=1
        for z in st.session_state.quiz:
            st.write(str(number) + ") " + z['explanation'])
            number += 1
  
