import streamlit as st
import model_load

# Streamlit App
st.title("Proteomics Chatbot")
st.write("Ask any question about proteins using their UniProt ID.")

# Chat Interface
query_from_user = st.text_input("Enter your question about a protein:")
if st.button("Ask"):
    if query_from_user:
        with st.spinner("Processing..."):
            try:
                # Step 1: Extract protein name
                protein_name = model_load.extract_protein_name(query_from_user)
                st.write(f"Extracted Protein Name: {protein_name}")
                
                # Step 2: Fetch and preprocess protein data
                context = model_load.fetch_protein_context(protein_name)
                
                # Step 3: Generate response
                response = model_load.generate_response(query_from_user, context)
                
                st.success("Chatbot Response:")
                st.write(response)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

# Display Chat History
if model_load.memory.chat_memory:
    st.subheader("Chat History")
    for message in model_load.memory.chat_memory.messages:
        st.markdown(f"**You:** {message.content}" if message.role == "user" else f"**Chatbot:** {message.content}")
