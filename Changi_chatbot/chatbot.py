import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_REGION")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = "changi-jewel-index"

def build_chatbot():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    embedding = HuggingFaceEmbeddings(model_name="WhereIsAI/UAE-Large-V1")

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embedding,
        text_key="text"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # ✅ This works only with Gemini API (not Vertex AI)
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0.2,
        google_api_key=GOOGLE_API_KEY
    )

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

if __name__ == "__main__":
    bot = build_chatbot()
    query = "Where can I eat at Jewel Changi?"
    response = bot.invoke(query)
    print("Answer:", response)
