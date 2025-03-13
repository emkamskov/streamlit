import json
import streamlit as st
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os

import dotenv


dotenv.load_dotenv()
giga = GigaChat(
    verify_ssl_certs=False,
    profanity_check=False,
    timeout=6000,
    model=os.getenv('MODEL'),
    credentials=os.getenv('CREDS'),
    scope=os.getenv('SCOPE'),
)

def evaluate_competency(user_info: dict, prompt: str) -> dict:
    """Оценивает компетенции на основе данных и промпта."""
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=prompt
            )
        ],
        temperature=0.7,
    )

    payload.messages.append(Messages(role=MessagesRole.USER, content=str(user_info)))

    response = giga.chat(payload)
    return json.loads(response.choices[0].message.content)

def main():
    st.title("Оценка компетенций сотрудника")

    with open("prompts/competency_prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()

    st.subheader("Введите данные о сотруднике")

    education = st.text_input("Образование", value="Высшее образование, MBA")
    courses = st.text_input("Курсы", value='Agile-курсы, Курсы по управлению проектами')
    experience = st.text_input("Опыт работы", value="10 лет в управлении командами")

    cognitive = st.slider("Когнитивные способности (1-100)", min_value=0, max_value=100, value=85)
    eq = st.slider("Эмоциональный интеллект (1-100)", min_value=0, max_value=100, value=90)

    colleagues_feedback = st.text_input("Отзывы коллег", value='Быстро обучается, Хорошо адаптируется к изменениям')
    manager_feedback = st.text_input("Отзывы руководителя", value='Иногда не хватает глубины анализа')

    self_reflection = st.text_input("Саморефлексия", value='Я стараюсь анализировать свои ошибки, но иногда не хватает времени')
    adaptability = st.text_input("Адаптивность", value='Я легко адаптируюсь к новым условиям и помогаю другим')

    if st.button("Оценить"):
        user_info = {
            "resume": {
                "education": education,
                "courses": courses.split(", "),
                "experience": experience
            },
            "test_results": {
                "cognitive": cognitive,
                "eq": eq
            },
            "feedback": {
                "colleagues": colleagues_feedback.split(", "),
                "manager": manager_feedback.split(", ")
            },
            "interview": {
                "self_reflection": self_reflection,
                "adaptability": adaptability
            }
        }

        result = evaluate_competency(user_info, prompt)
        
        st.subheader("Результат оценки:")
        st.json(result)

if __name__ == "__main__":
    main()