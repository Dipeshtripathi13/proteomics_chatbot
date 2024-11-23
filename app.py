import streamlit as st
import model_load
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

# Initialize memory for conversation history
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Function to update the conversation in memory
def update_chat_history(user_message, bot_message):
    # Add user input to memory
    st.session_state.memory.chat_memory.add_user_message(user_message)
    # Add bot response to memory
    st.session_state.memory.chat_memory.add_ai_message(bot_message)

# Streamlit App
st.title("Proteomics Chatbot")
st.write("Ask any question about proteins using their UniProt ID.")

# Display conversation history (Chat History)
if st.session_state.memory.chat_memory:
    st.subheader("Chat History")
    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            st.markdown(f"**You:** {message.content}")
        elif isinstance(message, AIMessage):
            st.markdown(f"**Chatbot:** {message.content}")

# Text input box for the user to type their question
query_from_user = st.text_input("You:", "")

# Button to send the query
if st.button("Ask"):
    if query_from_user:
        with st.spinner("Processing..."):
            try:
                # Step 1: Extract protein name from the user's query
                protein_name = model_load.extract_protein_name(query_from_user)
                st.write(f"Extracted Protein Name: {protein_name}")

                # Step 2: Fetch and preprocess protein data
                context = model_load.fetch_protein_context(protein_name)

                # Step 3: Generate the response using LangChain
                response = model_load.generate_response(query_from_user, context)

                # Step 4: Update chat history with the user's message and chatbot's response
                update_chat_history(query_from_user, response)

                # Display bot response
                st.success(f"**Chatbot:** {response}")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
