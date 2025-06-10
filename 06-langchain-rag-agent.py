from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

doc_path = "./docs/resume.pdf"
model = "llama3.2"

if doc_path:
    loader = UnstructuredPDFLoader(file_path=doc_path)
    data = loader.load()
    print("data loading")
else:
    print("No document.")

content = data[0].page_content

# print(content[:100])

# split and chunk
# greater the overlap greater the context
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)

print("done splitting..")

# print(chunks)

# Add to vector database
import ollama

ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="rag-db"
)

print("Done adding to vector db")

## Retrieval

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# setup model
llm = ChatOllama(model=model)

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""
       You are a smart assistant representing the person in document, acting on his behalf. You have access to person’s resume and will use it to answer questions confidently and professionally, in the first person as if you are Kishan.

        Objective: Given a question, read the resume to extract the most relevant information and answer naturally as if you are person speaking about yourself.
        Instructions:
        Do not guess or fabricate; answer only based on resume content.
        
        If the answer is not available in the resume, say: “That information isn’t included in my resume.”


        
        Original question: {question}
    """
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm,
    prompt=QUERY_PROMPT,
)

##RAG prompt
template = """
    Answer the question based ONLY on the following context and reply on person's behalf
    {context}
    
    Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough() }
    | prompt
    | llm
    | StrOutputParser()
)

# res = chain.invoke(input=("what is the document about ?"))

res = chain.invoke(input="what is your email and phone number?")
res = chain.invoke(input="what is your name and where are you from?")

print(res)
