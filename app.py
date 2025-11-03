import gradio as gr
import os
from dotenv import load_dotenv
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from typing import List
import uuid

# Load environment variables
load_dotenv()

# Initialize components globally
embedding_model = None
vector_db_client = None
vector_collection = None
gemini_model = None

# Global state
pdf_processed = False
current_pdf_name = ""

def extract_text_from_pdf(pdf_path: str) -> tuple:
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            return text, num_pages
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        if end < text_length:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size * 0.5:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks

def initialize_components():
    """Initialize all AI components"""
    global embedding_model, vector_db_client, vector_collection, gemini_model
    
    try:
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "❌ Error: GOOGLE_API_KEY not found in .env file!\n\nPlease create a .env file with:\nGOOGLE_API_KEY=your_key_here\n\nGet it from: https://makersuite.google.com/app/apikey"
        
        # Initialize embedding model
        print("Loading embedding model...")
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize ChromaDB
        print("Initializing vector database...")
        vector_db_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            is_persistent=False
        ))
        vector_collection = vector_db_client.get_or_create_collection(
            name="pdf_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize Google Gemini
        print("Initializing Google Gemini API...")
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        return "✅ Astra LLM initialized successfully!\n\n🎉 You can now upload your PDF and start studying!"
        
    except Exception as e:
        return f"❌ Error initializing Astra LLM:\n{str(e)}\n\nMake sure you have a valid GOOGLE_API_KEY in your .env file."

def process_pdf(pdf_file):
    """Process uploaded PDF file"""
    global pdf_processed, current_pdf_name, vector_collection
    
    if pdf_file is None:
        return "❌ Please upload a PDF file first", ""
    
    if embedding_model is None:
        return "❌ Please click 'Initialize Astra LLM' button first", ""
    
    try:
        # Extract text
        yield "📄 Extracting text from PDF...", ""
        text, num_pages = extract_text_from_pdf(pdf_file.name)
        
        if not text.strip():
            yield "❌ No text found in PDF. The PDF might be image-based or corrupted.", ""
            return
        
        # Chunk text
        yield "✂️ Splitting text into chunks...", ""
        chunks = chunk_text(text)
        
        if not chunks:
            yield "❌ Failed to process PDF text", ""
            return
        
        # Generate embeddings
        yield f"🧠 Generating embeddings for {len(chunks)} chunks (this may take a moment)...", ""
        embeddings = embedding_model.encode(chunks, show_progress_bar=False)
        
        # Clear and store in vector DB
        yield "💾 Storing in vector database...", ""
        
        # Clear previous data
        try:
            vector_db_client.delete_collection("pdf_documents")
        except:
            pass
        
        vector_collection = vector_db_client.get_or_create_collection(
            name="pdf_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Add documents
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        vector_collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=ids
        )
        
        # Success
        current_pdf_name = os.path.basename(pdf_file.name)
        pdf_processed = True
        
        info_msg = f"""
📚 **PDF Processed Successfully by Astra LLM!**

📄 **File:** {current_pdf_name}
📖 **Pages:** {num_pages}
📝 **Words:** {len(text.split()):,}
🧩 **Chunks Created:** {len(chunks)}

✅ **Ready!** You can now:
- Ask questions in the chat
- Generate practice questions
- Get summaries and key points
"""
        
        yield "✅ PDF processed successfully! 🎉", info_msg
        
    except Exception as e:
        yield f"❌ Error processing PDF: {str(e)}", ""

def generate_with_gemini(prompt: str) -> str:
    """Generate text using Google Gemini"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def chat_with_pdf(message, history):
    """Answer questions about the PDF"""
    global pdf_processed, vector_collection, embedding_model, gemini_model
    
    if not pdf_processed:
        return "⚠️ Please upload and process a PDF first!"
    
    if not message.strip():
        return "⚠️ Please enter a question!"
    
    try:
        # Generate query embedding
        query_embedding = embedding_model.encode([message])[0]
        
        # Search vector database
        results = vector_collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=3
        )
        
        if not results["documents"][0]:
            return "❌ No relevant information found in the document."
        
        # Generate answer with Gemini
        context = "\n\n".join(results["documents"][0])
        
        prompt = f"""You are Astra LLM, a helpful AI study assistant. Answer the student's question based ONLY on the provided context from their study material.

Context from study material:
{context}

Student's Question: {message}

Instructions:
- Answer based only on the provided context
- If the answer is not in the context, say "I couldn't find this information in your study material"
- Be clear, concise, and helpful
- Use examples from the context when relevant

Answer:"""
        
        answer = generate_with_gemini(prompt)
        return answer
        
    except Exception as e:
        return f"❌ Error generating answer: {str(e)}"

def generate_questions(num_questions):
    """Generate practice questions from the PDF"""
    global pdf_processed, vector_collection, embedding_model, gemini_model
    
    if not pdf_processed:
        return "⚠️ Please upload and process a PDF first!"
    
    try:
        # Get relevant chunks
        dummy_query = embedding_model.encode(["generate practice questions"])[0]
        results = vector_collection.query(
            query_embeddings=[dummy_query.tolist()],
            n_results=5
        )
        
        if not results["documents"][0]:
            return "❌ No content available to generate questions."
        
        context = "\n\n".join(results["documents"][0])
        
        prompt = f"""You are Astra LLM. Based on the following study material, generate {num_questions} practice questions that would help a student prepare for an exam.

Study Material:
{context}

Instructions:
- Create diverse question types (multiple choice, short answer, conceptual questions)
- Focus on key concepts and important information
- Make questions challenging but fair
- Include a mix of difficulty levels
- Number each question clearly

Generate {num_questions} practice questions:"""
        
        questions = generate_with_gemini(prompt)
        return questions
        
    except Exception as e:
        return f"❌ Error generating questions: {str(e)}"

def generate_summary():
    """Generate summary of the PDF"""
    global pdf_processed, vector_collection, embedding_model, gemini_model
    
    if not pdf_processed:
        return "⚠️ Please upload and process a PDF first!"
    
    try:
        # Get chunks for summary
        dummy_query = embedding_model.encode(["summarize document"])[0]
        results = vector_collection.query(
            query_embeddings=[dummy_query.tolist()],
            n_results=10
        )
        
        if not results["documents"][0]:
            return "❌ No content available to summarize."
        
        context = "\n\n".join(results["documents"][0][:5])  # Limit context for summary
        
        prompt = f"""You are Astra LLM. Summarize the following study material in a clear and concise way. Focus on the main concepts and key points.

Study Material:
{context}

Provide a well-structured summary with:
1. Main topics covered
2. Key concepts and definitions
3. Important points to remember

Summary:"""
        
        summary = generate_with_gemini(prompt)
        return summary
        
    except Exception as e:
        return f"❌ Error generating summary: {str(e)}"

def get_key_points():
    """Extract key points from the PDF"""
    global pdf_processed, vector_collection, embedding_model, gemini_model
    
    if not pdf_processed:
        return "⚠️ Please upload and process a PDF first!"
    
    try:
        # Get chunks for key points
        dummy_query = embedding_model.encode(["extract key points"])[0]
        results = vector_collection.query(
            query_embeddings=[dummy_query.tolist()],
            n_results=8
        )
        
        if not results["documents"][0]:
            return "❌ No content available."
        
        context = "\n\n".join(results["documents"][0][:5])
        
        prompt = f"""You are Astra LLM. Extract the most important key points from the following study material. Present them as a clear bullet-point list.

Study Material:
{context}

Extract 7-10 key points that a student should focus on for exam preparation:"""
        
        key_points = generate_with_gemini(prompt)
        return key_points
        
    except Exception as e:
        return f"❌ Error extracting key points: {str(e)}"

# Create Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="Astra LLM") as demo:
    
    # Header
    gr.Markdown("""
    # ✨ Astra LLM
    ### Your AI-Powered Study Companion
    Upload your study material and let Astra help you learn smarter, not harder!
    """)
    
    # Initialization
    with gr.Row():
        init_btn = gr.Button("🚀 Initialize Astra LLM", variant="primary", size="lg")
        init_status = gr.Textbox(label="System Status", interactive=False, lines=3)
    
    init_btn.click(initialize_components, outputs=init_status)
    
    gr.Markdown("---")
    
    # Main Interface
    with gr.Row():
        # Left Column - Upload
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload Your Study Material")
            pdf_upload = gr.File(
                label="Drop your PDF here or click to browse",
                file_types=[".pdf"],
                type="filepath"
            )
            process_btn = gr.Button("🔄 Process PDF", variant="primary", size="lg")
            process_status = gr.Textbox(label="Processing Status", interactive=False)
            pdf_info = gr.Markdown()
            
            process_btn.click(
                process_pdf,
                inputs=pdf_upload,
                outputs=[process_status, pdf_info]
            )
        
        # Right Column - Chat
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Ask Astra Anything")
            chatbot = gr.Chatbot(height=400, label="Chat with Astra")
            msg = gr.Textbox(
                label="Your Question",
                placeholder="Ask Astra anything about your study material...",
                lines=2
            )
            
            msg.submit(chat_with_pdf, inputs=[msg, chatbot], outputs=chatbot)
            msg.submit(lambda: "", None, msg)
    
    gr.Markdown("---")
    
    # Features Row
    gr.Markdown("### 🎯 Quick Study Tools")
    
    with gr.Row():
        # Practice Questions
        with gr.Column():
            gr.Markdown("#### 📝 Practice Questions")
            num_questions = gr.Slider(
                minimum=3,
                maximum=10,
                value=5,
                step=1,
                label="Number of Questions"
            )
            gen_questions_btn = gr.Button("Generate Questions", variant="secondary", size="lg")
            questions_output = gr.Markdown(label="Generated Questions")
            
            gen_questions_btn.click(
                generate_questions,
                inputs=num_questions,
                outputs=questions_output
            )
        
        # Summary
        with gr.Column():
            gr.Markdown("#### 📋 Smart Summary")
            gen_summary_btn = gr.Button("Generate Summary", variant="secondary", size="lg")
            summary_output = gr.Markdown(label="Summary")
            
            gen_summary_btn.click(
                generate_summary,
                outputs=summary_output
            )
        
        # Key Points
        with gr.Column():
            gr.Markdown("#### 🎯 Key Points")
            gen_keypoints_btn = gr.Button("Extract Key Points", variant="secondary", size="lg")
            keypoints_output = gr.Markdown(label="Key Points")
            
            gen_keypoints_btn.click(
                get_key_points,
                outputs=keypoints_output
            )
    
    # Footer
    gr.Markdown("""
    ---
    ### 💡 Pro Tips:
    - Upload clear, text-based PDFs for best results
    - Ask specific questions to get detailed answers
    - Use practice questions to test your knowledge before exams
    - Save summaries and key points for quick revision
    
    **Powered by Astra LLM & Google Gemini** ✨ | Built with Gradio
    """)

# Launch the app
if __name__ == "__main__":
    print("🚀 Starting Astra LLM...")
    print("📍 Access the app at: http://localhost:8080")
    demo.launch(server_name="0.0.0.0", server_port=8080)