import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import json

def show_ui(on_generate, on_refine):
    st.set_page_config(
        page_title="Tweetify AI",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 18px;
            color: #6d6d6d;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🚀 Tweetify AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Repurpose your articles into viral LinkedIn, X (Twitter), and Instagram posts in seconds!</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("Using Mistral AI (mistralai-small-2506) backend.")
        
        if st.button("🔄 Clear Chat & Restart", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.generated_posts = None
            st.success("History cleared!")
            st.rerun()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📝 Input Article / Text")
        user_article = st.text_area(
            "Paste your article or long-form content here:", 
            height=300,
            placeholder="Type or paste your content..."
        )
        
        generate_btn = st.button("⚡ Generate Viral Posts", type="primary", use_container_width=True)

        if generate_btn:
            if not user_article.strip():
                st.warning("Please paste some content first!")
            else:
                on_generate(user_article)

    with col2:
        st.subheader("✨ Your Social Posts")
        
        if st.session_state.generated_posts:
            posts = st.session_state.generated_posts
            
            tab1, tab2, tab3 = st.tabs(["📄 LinkedIn", "🐦 X (Twitter) Thread", "📸 Instagram Caption"])
            
            with tab1:
                st.markdown("### **LinkedIn Post**")
                st.code(posts.get("linkedin", ""), language="text", wrap_lines=True)
                
            with tab2:
                st.markdown("### **X (Twitter) Thread**")
                tweets = posts.get("twitter", [])
                if isinstance(tweets, list):
                    for idx, tweet in enumerate(tweets, 1):
                        st.markdown(f"**Tweet {idx}/{len(tweets)}**")
                        st.code(tweet, language="text", wrap_lines=True)
                else:
                    st.code(tweets, language="text", wrap_lines=True)
                    
            with tab3:
                st.markdown("### **Instagram Caption**")
                st.code(posts.get("instagram", ""), language="text", wrap_lines=True)
                
            st.markdown("---")
            st.markdown("### 💬 Want to modify or adjust these posts?")
            refinement_input = st.chat_input("e.g., Make the LinkedIn post shorter, or make the tweets funnier...")
            
            if refinement_input:
                on_refine(refinement_input)
                        
        else:
            st.info("Your generated posts will appear here once you hit 'Generate Viral Posts'.")