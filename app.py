import streamlit as st
from src.classifier import classify_persona
from src.vector_store import search_similar_chunks, format_search_results, initialize_vector_store
from src.generator import generate_adaptive_response
from src.ai_utils import retry_ai_call, is_temporary_ai_error

st.set_page_config(page_title="ResolveAI", page_icon="🤖", layout="wide")

initialize_vector_store()

st.markdown("# 🤖 ResolveAI")
st.markdown("### AI Customer Support Platform")

user_query = st.text_area('Enter your query here:', height=150, placeholder="Example: I forgot my password and I am not receiving the OTP.")

if st.button('Generate response'):
    try:
        if not user_query.strip():
            st.warning("Please enter a valid query")
            st.stop()

        with st.spinner('Analyzing query...'):
            classification = retry_ai_call(classify_persona, user_query)

            persona = classification['persona']
            confidence = classification['confidence']
            reasoning = classification['reasoning']

            results = search_similar_chunks(user_query)
            context_chunks = format_search_results(results)

            response = retry_ai_call(generate_adaptive_response, user_query, persona, context_chunks)
        
        st.subheader("Detected Persona:")
            
        st.markdown(f"**Persona:** {persona}")
        st.markdown(f"**Confidence:** {confidence * 100:.0f}%")
        st.markdown(f"**Reasoning:** {reasoning}")

        st.subheader("AI Response")
        if response['escalated']:
            st.warning("This query has been escalated to a human support specialist.")
            st.markdown(response['response'])

            st.subheader("Handoff Summary:")
            st.code(response['handoff_summary'], language='json')
        else:
            st.success("Resolved using knowledge base.")
            st.markdown(response['response'])
        
        st.subheader("Files Used")
        sources = sorted(set(chunk['source'] for chunk in context_chunks))
        if sources:
            for source in sources:
                    st.markdown(f"- {source}")
        else:
            st.info("No files were retrieved.")

    except Exception as e:
        if is_temporary_ai_error(e):
            st.warning(
                "ResolveAI is temporarily experiencing high demand from the AI service.\n\n"
                "Please wait a few moments and try again."
            )
        else:
            st.error(
                "Something went wrong while generating the response."
            )