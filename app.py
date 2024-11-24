import streamlit as st
import random
import time
import model_load

# Initialize the app
st.title("Proteomics Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about a protein..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show processing indicator
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Step 1: Extract protein name from the user's query
            protein_name = model_load.extract_protein_name(prompt)

            # Step 2: Fetch and preprocess protein data
            context = model_load.fetch_protein_context(protein_name)

            # Step 3: Generate the response using LangChain
            response = model_load.generate_response(prompt, context)

            # Streamed response emulator
            def response_generator():
                for word in response.split():
                    yield word + " "
                    time.sleep(0.05)  # Simulating typewriter effect

            # Display assistant response in chat message container with streaming
            st.write_stream(response_generator())

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Refresh the app and update the chat history
            st.rerun()   # This will force a rerun of the app and refresh the chat history
