import streamlit as st
import json
from src.backend import generate_social_posts
# इम्पोर्ट पाथ अब सीधे और आसान हो गया है ⬇️
from frontend import show_ui
from langchain_core.messages import HumanMessage, AIMessage

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "generated_posts" not in st.session_state:
    st.session_state.generated_posts = None

def handle_generation(user_article):
    with st.spinner("🧠 Mistral is crafting your social posts..."):
        try:
            result = generate_social_posts(user_article, st.session_state.chat_history)
            st.session_state.generated_posts = result
            st.session_state.chat_history.append(HumanMessage(content=user_article))
            st.session_state.chat_history.append(AIMessage(content=json.dumps(result)))
            st.success("Posts generated successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

def handle_refinement(refinement_input):
    with st.spinner("Updating posts based on your feedback..."):
        try:
            result = generate_social_posts(refinement_input, st.session_state.chat_history)
            st.session_state.generated_posts = result
            st.session_state.chat_history.append(HumanMessage(content=refinement_input))
            st.session_state.chat_history.append(AIMessage(content=json.dumps(result)))
            st.rerun()
        except Exception as e:
            st.error(f"Error updating posts: {str(e)}")

if __name__ == "__main__":
    show_ui(on_generate=handle_generation, on_refine=handle_refinement)