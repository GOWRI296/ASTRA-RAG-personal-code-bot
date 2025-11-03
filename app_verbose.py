print('🚀 Starting Astra LLM...')
print('📦 Loading libraries (this may take a minute)...')

import gradio as gr
print('✓ Gradio loaded')

import os
from dotenv import load_dotenv
print('✓ Environment loaded')

import PyPDF2
print('✓ PDF reader loaded')

print('⏳ Loading AI model (this is the slow part - be patient)...')
from sentence_transformers import SentenceTransformer
print('✓ Sentence Transformers loaded')

import chromadb
from chromadb.config import Settings
print('✓ ChromaDB loaded')

from huggingface_hub import InferenceClient
print('✓ Hugging Face client loaded')

from typing import List
import uuid

print('✅ All libraries loaded! Starting app...')
print('=' * 50)

# [Rest of your app.py code goes here - copy everything after the imports]
