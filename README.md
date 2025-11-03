Astra LLM - AI-Powered Study Companion
An intelligent RAG (Retrieval-Augmented Generation) chatbot that helps students study smarter by analyzing PDF documents and providing interactive Q&A, summaries, and practice questions.

🌟 Astra LLM - AI-Powered Study Companion
An intelligent RAG (Retrieval-Augmented Generation) chatbot that helps students study smarter by analyzing PDF documents and providing interactive Q&A, summaries, and practice questions.
Show Image
Show Image
✨ Features

📄 PDF Processing: Upload and analyze your study materials
💬 Interactive Chat: Ask questions and get instant answers from your documents
📝 Practice Questions: Generate custom practice questions for exam prep
📋 Smart Summaries: Get concise summaries of lengthy content
🎯 Key Points Extraction: Identify the most important concepts
🧠 Vector Search: Fast and accurate information retrieval using semantic search

🛠️ Technologies Used

Gradio - Modern web interface
Google Gemini - Advanced LLM for answer generation
Sentence Transformers - High-quality text embeddings
ChromaDB - Vector database for semantic search
PyPDF2 - PDF text extraction

📋 Prerequisites
Before you begin, make sure you have:

Python 3.9 or higher installed
pip (Python package installer)
A Google Gemini API key (Get it free here)

🚀 Installation
Step 1: Download the Project
Create a new folder for your project:
bashmkdir astra-llm
cd astra-llm
Step 2: Add Project Files
Make sure you have these files in your folder:

app.py (main application code)
requirements.txt (dependencies)
.env.example (environment template)

Step 3: Create Virtual Environment
bash# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
You should see (venv) in your terminal prompt.
Step 4: Install Dependencies
bashpip install -r requirements.txt
This will install all required packages. It may take a few minutes.
Step 5: Set Up Environment Variables

Create a .env file in your project folder:

bash# On Windows:
copy .env.example .env

# On macOS/Linux:
cp .env.example .env

Open .env file and add your Google API key:

GOOGLE_API_KEY=your_actual_api_key_here

Get your API key from: https://makersuite.google.com/app/apikey

Step 6: Run the Application
bashpython app.py
You should see:
🚀 Starting Astra LLM...
📍 Access the app at: http://localhost:8080
Step 7: Open in Browser
Open your web browser and go to: http://localhost:8080
📖 How to Use
Getting Started

Initialize Astra LLM

Click the "🚀 Initialize Astra LLM" button
Wait for all components to load (this may take 1-2 minutes on first run)
You'll see "✅ Astra LLM initialized successfully!"


Upload Your PDF

Click on the upload area or drag & drop your PDF file
Click "🔄 Process PDF" button
Wait for processing to complete
You'll see details about your document (pages, words, chunks)


Start Learning!

Feature Guide
💬 Chat with Astra

Type your question in the text box
Press Enter or click submit
Astra will answer based on your uploaded document
Ask follow-up questions for deeper understanding

Example Questions:

"What are the main topics covered in this chapter?"
"Explain the concept of X in simple terms"
"What are the differences between A and B?"

📝 Practice Questions

Select number of questions (3-10)
Click "Generate Questions"
Get a mix of multiple choice, short answer, and conceptual questions
Use these to test your knowledge before exams

📋 Smart Summary

Click "Generate Summary" button
Get a concise overview of your document
Perfect for quick revision before tests
Includes main topics, key concepts, and important points

🎯 Key Points

Click "Extract Key Points" button
Get 7-10 most important concepts
Focus on these for efficient studying
Great for last-minute review

📁 Project Structure
astra-llm/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .env                    # Your API key (YOU CREATE THIS)
├── .env.example           # Template for .env
├── README.md              # This documentation
├── .gitignore             # Git ignore file
│
└── venv/                  # Virtual environment (auto-generated)
    ├── Lib/
    ├── Scripts/
    └── ...
💡 Tips for Best Results
PDF Upload Tips

✅ Use text-based PDFs (not scanned images)
✅ Ensure PDFs are not password-protected
✅ Clear, well-formatted documents work best
✅ Recommended size: Under 50 pages for faster processing

Question Tips

✅ Ask specific questions for detailed answers
✅ Reference specific topics or sections
✅ Ask for examples or explanations
❌ Avoid very vague or general questions

Study Tips

📚 Process one topic/chapter at a time
🎯 Use practice questions regularly
📝 Save key points for quick revision
🔄 Re-generate questions for variety

🐛 Troubleshooting
Issue: "GOOGLE_API_KEY not found"
Solution:

Make sure you created .env file (not .env.example)
Open .env and check your API key is added correctly
No quotes needed: GOOGLE_API_KEY=AIza...
Restart the application

Issue: "PDF Processing Failed"
Solution:

Ensure PDF contains extractable text (not scanned images)
Try a different PDF file
Check if file is corrupted
Make sure file is not password-protected

Issue: "Slow Response Times"
Solution:

First initialization downloads models (1-2 GB) - this is normal
Subsequent runs will be much faster
Large PDFs (50+ pages) take longer to process
Check your internet connection for API calls

Issue: "Module Not Found Error"
Solution:

Make sure virtual environment is activated (you see (venv))
Run: pip install -r requirements.txt again
Check you're using Python 3.9+: python --version

Issue: "Port 8080 Already in Use"
Solution:

Stop any other applications using port 8080
Or modify app.py line 463 to use different port:

python   demo.launch(server_name="0.0.0.0", server_port=8081)
⚙️ System Requirements

Operating System: Windows 10+, macOS 10.14+, or Linux
RAM: 4GB minimum, 8GB recommended
Storage: 2-3GB for models and dependencies
Internet: Required for:

First-time model download
Google Gemini API calls
Initial setup



🔒 Privacy & Security

Your documents are processed locally
Only text chunks are sent to Google Gemini API
No documents are permanently stored
API key is kept in local .env file
Clear vector database on each new PDF upload

🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch
Make your changes
Submit a pull request

📄 License
This project is open-source and available under the MIT License.
🆘 Support
Need help?

📧 Create an issue on GitHub
📚 Check this README's troubleshooting section
🔗 Review Google Gemini API docs
🔗 Check Gradio documentation

🙏 Acknowledgments
Built with amazing open-source tools:

Gradio - UI framework
Google Gemini - LLM API
ChromaDB - Vector database
Sentence Transformers - Embeddings
