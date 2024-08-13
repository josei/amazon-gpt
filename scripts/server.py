import streamlit as st
from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate

Settings.llm = Ollama(model="llama3", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="Snowflake/snowflake-arctic-embed-m", trust_remote_code=True)

@st.cache_resource
def load_engine():
    loader = SimpleDirectoryReader(
        input_dir='data/gold',
        required_exts=['.md'],
        recursive=True
    )
    docs = loader.load_data()
    index = VectorStoreIndex.from_documents(docs)
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=4)

    template = "Context information is below. \n"
    template += "-------------\n"
    template += "{context_str}\n\n"
    template += "Given the context information above I want you \n"
    template += "to think step by step to answer the query in a crisp\n"
    template += "manner, in case you don't know the answer say 'I don't know!'\n"
    template += "Query: {query_str}\n"
    template += "Answer: "

    query_engine.update_prompts({"response_synthesizer:text_qa_template": PromptTemplate(template)})

    return query_engine

def main():
    st.title('AmazonGPT')
    engine = load_engine()

    user_input = st.text_area("Ask for some Amazon product:", "Can you recommend me a book light that will not disturb my partner? Please include product ID and relevant reviews")

    if st.button("Ask AmazonGPT"):
        with st.spinner("Thinking..."):
            message_placeholder = st.empty()
            response = engine.query(user_input)
            full_response = ""
            for chunk in response.response_gen:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

if __name__ == "__main__":
    main()