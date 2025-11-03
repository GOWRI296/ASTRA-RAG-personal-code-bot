import sys
import traceback

print('='*60)
print('STARTING ASTRA LLM - DEBUG MODE')
print('='*60)

try:
    print('\n[1/5] Importing Gradio...')
    import gradio as gr
    print('     ✓ Gradio OK')
    
    print('\n[2/5] Importing utilities...')
    import os
    from dotenv import load_dotenv
    import PyPDF2
    from typing import List
    import uuid
    print('     ✓ Utilities OK')
    
    print('\n[3/5] Loading AI model (THIS TAKES TIME - BE PATIENT)...')
    from sentence_transformers import SentenceTransformer
    print('     ✓ Model imported')
    
    print('\n[4/5] Importing vector database...')
    import chromadb
    from chromadb.config import Settings
    from huggingface_hub import InferenceClient
    print('     ✓ Database OK')
    
    print('\n[5/5] Loading main app...')
    with open('app.py', 'r', encoding='utf-8') as f:
        code = f.read()
        exec(code)
    
except KeyboardInterrupt:
    print('\n\n❌ App stopped by user')
    sys.exit(0)
    
except Exception as e:
    print('\n\n' + '='*60)
    print('❌ ERROR FOUND!')
    print('='*60)
    print(f'\nError Type: {type(e).__name__}')
    print(f'Error Message: {str(e)}')
    print('\nFull Traceback:')
    print('-'*60)
    traceback.print_exc()
    print('='*60)
    sys.exit(1)
