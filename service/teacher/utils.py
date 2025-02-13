from langchain_community.document_loaders import OnlinePDFLoader, PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
import os

# load the dotenv credentials
load_dotenv()

# configuring Google Gemini API
apiKey = os.getenv('GOOGLE_API_KEY')

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = apiKey

print("Gemini API Key set successfully!")

# configuring PineCone API Credentials
pineconeKey = os.getenv('PINECONE_API_KEY')

if "PINECONE_API_KEY" not in os.environ:
    os.environ["PINECONE_API_KEY"] = pineconeKey

print("PineCone API Key set successfully!")

# generate system prompt
class SystemPrompt:
    def __init__(self) -> None:
        pass

    def generate_system_context(self):
        system_context = ("""You are an AI-powered teacher designed to provide clear, educational, and engaging answers to students' questions. 
            Your goal is to explain concepts concisely while ensuring understanding. 
            Encourage curiosity, provide examples when necessary, and simplify complex ideas without losing accuracy.

            Keep your responses informative yet concise. 
            Avoid unnecessary details but provide depth where required. 
            Use simple language for younger students and adjust explanations based on the question’s complexity.

            {context}
            """)
        
        return system_context

# 🔹 Pinecone Connector Class
class PineConeConnector:
    def __init__(self, uid, chunks, embedder) -> None:
        self.uid = uid
        self.embedder = embedder
        self.chunks = chunks
        self.index_name = f"teacher-user-{self.uid}"

        # Initialize Pinecone once
        self.pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

        # Create index if it doesn't exist
        if self.index_name not in [i.name for i in self.pc.list_indexes()]:
            self.pc.create_index(
                name=self.index_name,
                dimension=768,  # Update this based on your model's dimension
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

    def upload_to_pinecone(self):
        """Uploads document chunks to Pinecone."""
        doc_store = PineconeVectorStore.from_documents(
            documents=self.chunks,
            index_name=self.index_name,
            embedding=self.embedder,
        )
        return doc_store

    def get_retriever(self):
        """Retrieves stored embeddings from Pinecone."""
        doc_store = PineconeVectorStore.from_existing_index(
            index_name=self.index_name,
            embedding=self.embedder,
        )
        retriever = doc_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        return retriever

# 🔹 Gemini RAG Class
class GeminiRag:
    def __init__(self, uid, chunks, embedder, question):
        self.question = question

        # Initialize Pinecone storage
        self.pinecone_connector = PineConeConnector(uid, chunks, embedder)
        
        # Upload chunks and get retriever
        self.pinecone_connector.upload_to_pinecone()
        self.retriever = self.pinecone_connector.get_retriever()

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.9)

        # Generate system context and set up prompt template
        system_context = SystemPrompt().generate_system_context()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_context),
                ("human", "{input}"),
            ]
        )

    def answer_question(self):
        """Retrieves documents and answers the question."""
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)

        return rag_chain.invoke({"input": self.question})
    
# embedder class
class GetEmbedder:
    def __init__(self):
        pass

    def embedding_instance_provider(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return embeddings
    
# class for creating file Instance
class FileInstanceCreator:
    def __init__(self, url : str) -> None:
        self.url = url

    def file_loader(self):
        loader = DirectoryLoader(self.url,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )

        document = loader.load()
        return document
    
# chunking of the data
class Chunker:
    def __init__(self, text: str, chunk_size: int = 500) -> None:
        self.text = text
        self.chunk_size = chunk_size

    def chunk(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = 20
        )

        text_chunks = text_splitter.split_documents(self.text)
        return text_chunks
    
class AppwritePdfReader:
    def __init__(self, url):
        self.url = url

    def loader_instance_online(self):
        online_pdf_loader = OnlinePDFLoader(url=self.url)
        document = online_pdf_loader.load()
        return document