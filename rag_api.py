from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
llm = ChatGroq(api_key="your_key", model="llama-3.3-70b-versatile")
prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. If answer is not in the context, say "i don't have the information"
context : {context}
question : {question}
""")
chain = prompt | llm
loader = TextLoader('artik_info.txt')
document = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap = 20)
chunks = splitter.split_documents(document)
embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings)
print("vectordb created.")
class question(BaseModel):
    question : str
@app.post("/ask")
def ask_question(data : question):
    user_question = data.question
    results = vectorstore.similarity_search(user_question, k=2)
    context = "\n".join([r.page_content for r in results])
    response = chain.invoke({"context":context, "question": user_question})
    print(f"answer : {response.content}")
    print("function is working")
    return {"answer" : response.content}