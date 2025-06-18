import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
import tempfile
import json

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Please set GROQ_API_KEY environment variable")
    st.stop()

client = Groq(api_key=groq_api_key)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def ask_groq_question(context, question, model="llama3-8b-8192"):
    """Ask a question to Groq API based on the PDF context"""
    try:
        prompt = f"""Based on the following PDF content, please answer the question. 
        If the answer cannot be found in the content, please say so.

        PDF Content:
        {context}

        Question: {question}

        Answer:"""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0.1,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="PDF Question Answering with Groq",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 PDF Question Answering with Groq")
    st.markdown("Upload a PDF file and ask questions about its content using Groq's LLM.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        model = st.selectbox(
            "Choose Groq Model",
            ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### Instructions")
        st.markdown("""
        1. Upload a PDF file
        2. Wait for text extraction
        3. Ask questions about the content
        4. Get AI-powered answers
        """)
        
        st.markdown("---")
        st.markdown("**Note:** Make sure to set your `GROQ_API_KEY` environment variable")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF file to extract text and ask questions about it"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                pdf_text = extract_text_from_pdf(uploaded_file)
            
            if pdf_text:
                # Store in session state
                st.session_state['pdf_text'] = pdf_text
                st.session_state['pdf_name'] = uploaded_file.name
                
                # Show text preview
                with st.expander("📖 PDF Text Preview (first 500 characters)"):
                    st.text(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
                
                st.success(f"✅ Extracted {len(pdf_text)} characters from PDF")
            else:
                st.error("❌ Failed to extract text from PDF")
    
    with col2:
        st.header("❓ Ask Questions")
        
        if 'pdf_text' not in st.session_state:
            st.info("👆 Please upload a PDF file first")
        else:
            st.info(f"📄 Current PDF: {st.session_state['pdf_name']}")
            
            # Question input
            question = st.text_area(
                "Enter your question about the PDF content:",
                placeholder="What is the main topic of this document?",
                height=100
            )
            
            if st.button("🚀 Ask Groq", type="primary"):
                if question.strip():
                    with st.spinner("🤔 Thinking..."):
                        answer = ask_groq_question(
                            st.session_state['pdf_text'],
                            question,
                            model
                        )
                    
                    st.markdown("### 💡 Answer")
                    st.write(answer)
                    
                    # Store in chat history
                    if 'chat_history' not in st.session_state:
                        st.session_state['chat_history'] = []
                    
                    st.session_state['chat_history'].append({
                        'question': question,
                        'answer': answer,
                        'model': model
                    })
                else:
                    st.warning("Please enter a question")
            
            # Chat history
            if 'chat_history' in st.session_state and st.session_state['chat_history']:
                st.markdown("---")
                st.markdown("### 💬 Chat History")
                
                for i, chat in enumerate(reversed(st.session_state['chat_history'])):
                    with st.expander(f"Q: {chat['question'][:50]}..."):
                        st.markdown(f"**Question:** {chat['question']}")
                        st.markdown(f"**Answer:** {chat['answer']}")
                        st.caption(f"Model: {chat['model']}")
                        
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            st.session_state['chat_history'].pop(-(i+1))
                            st.rerun()

if __name__ == "__main__":
    main() 