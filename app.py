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

def ask_groq_with_confidence(context, question, model="llama3-8b-8192"):
    """Ask question and get confidence score"""
    try:
        prompt = f"""Answer the question based on the provided content and rate your confidence.

PDF Content:
{context}

Question: {question}

Provide your answer in this exact format:
ANSWER: [your answer here]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASONING: [brief explanation of why you're confident or not]

Rules:
- HIGH: Information is clearly stated in the text
- MEDIUM: Information is implied or partially stated
- LOW: Information is not found or very unclear
- If no relevant information exists, say "I cannot find information about this in the provided document." """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.0,
            max_tokens=1024,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Parse the response
        lines = response.split('\n')
        answer = ""
        confidence = "UNKNOWN"
        reasoning = ""
        
        for line in lines:
            if line.startswith("ANSWER:"):
                answer = line.replace("ANSWER:", "").strip()
            elif line.startswith("CONFIDENCE:"):
                confidence = line.replace("CONFIDENCE:", "").strip()
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()
        
        return {
            "answer": answer,
            "confidence": confidence,
            "reasoning": reasoning,
            "full_response": response
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "confidence": "ERROR",
            "reasoning": "Failed to process request",
            "full_response": ""
        }

def ask_groq_with_sources(context, question, model="llama3-8b-8192"):
    """Ask question and provide source citations"""
    try:
        prompt = f"""Answer the question based on the provided content and cite specific parts of the text.

PDF Content:
{context}

Question: {question}

Provide your answer in this format:
ANSWER: [your answer here]
SOURCES: [quote the specific text that supports your answer]
CONFIDENCE: [HIGH/MEDIUM/LOW based on how clearly the information is stated]

If the information is not in the text, respond with:
ANSWER: I cannot find information about this in the provided document.
SOURCES: None
CONFIDENCE: NONE"""

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.0,
            max_tokens=1024,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Parse the response
        lines = response.split('\n')
        answer = ""
        sources = ""
        confidence = "UNKNOWN"
        
        current_section = ""
        for line in lines:
            if line.startswith("ANSWER:"):
                answer = line.replace("ANSWER:", "").strip()
                current_section = "answer"
            elif line.startswith("SOURCES:"):
                sources = line.replace("SOURCES:", "").strip()
                current_section = "sources"
            elif line.startswith("CONFIDENCE:"):
                confidence = line.replace("CONFIDENCE:", "").strip()
                current_section = "confidence"
            elif line.strip() and current_section == "sources":
                sources += " " + line.strip()
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "full_response": response
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "sources": "Error occurred",
            "confidence": "ERROR",
            "full_response": ""
        }

def main():
    st.set_page_config(
        page_title="PDF Question Answering with Groq",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 PDF Question Answering with Groq")
    st.markdown("Upload a PDF file and ask questions about its content using Groq's LLM with **hallucination prevention**.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        model = st.selectbox(
            "Choose Groq Model",
            ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 🛡️ Hallucination Prevention")
        use_confidence = st.checkbox("Show confidence scores", value=True, help="LLM rates its own confidence in the answer")
        use_sources = st.checkbox("Show source citations", value=True, help="Show exact text that supports the answer")
        
        if use_confidence:
            st.info("""
            **What does the confidence score mean?**
            - **HIGH**: The answer is clearly stated in the document.
            - **MEDIUM**: The answer is implied or partially stated.
            - **LOW**: The answer is not found or is very unclear.
            """)
        
        st.markdown("---")
        st.markdown("### Instructions")
        st.markdown("""
        1. Upload a PDF file
        2. Wait for text extraction
        3. Ask questions about the content
        4. Get AI-powered answers with confidence scores
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
                        if use_confidence and use_sources:
                            # Use both confidence and sources
                            result = ask_groq_with_sources(
                                st.session_state['pdf_text'],
                                question,
                                model
                            )
                            
                            st.markdown("### 💡 Answer")
                            st.write(result["answer"])
                            
                            # Color-code confidence
                            if result["confidence"] == "HIGH":
                                st.success(f"✅ **Confidence:** {result['confidence']}")
                            elif result["confidence"] == "MEDIUM":
                                st.warning(f"⚠️ **Confidence:** {result['confidence']}")
                            elif result["confidence"] == "LOW":
                                st.error(f"❌ **Confidence:** {result['confidence']}")
                            else:
                                st.info(f"ℹ️ **Confidence:** {result['confidence']}")
                            
                            # Show sources
                            if result["sources"] and result["sources"].lower() != "none":
                                with st.expander("📚 Source Citations"):
                                    st.markdown(result["sources"])
                            else:
                                st.info("📚 **Sources:** No specific citations available")
                        
                        elif use_confidence:
                            # Use confidence scoring only
                            result = ask_groq_with_confidence(
                                st.session_state['pdf_text'],
                                question,
                                model
                            )
                            
                            st.markdown("### 💡 Answer")
                            st.write(result["answer"])
                            
                            # Color-code confidence
                            if result["confidence"] == "HIGH":
                                st.success(f"✅ **Confidence:** {result['confidence']}")
                            elif result["confidence"] == "MEDIUM":
                                st.warning(f"⚠️ **Confidence:** {result['confidence']}")
                            elif result["confidence"] == "LOW":
                                st.error(f"❌ **Confidence:** {result['confidence']}")
                            else:
                                st.info(f"ℹ️ **Confidence:** {result['confidence']}")
                            
                            st.markdown(f"**Reasoning:** {result['reasoning']}")
                        
                        elif use_sources:
                            # Use source citations only
                            result = ask_groq_with_sources(
                                st.session_state['pdf_text'],
                                question,
                                model
                            )
                            
                            st.markdown("### 💡 Answer")
                            st.write(result["answer"])
                            
                            # Show sources
                            if result["sources"] and result["sources"].lower() != "none":
                                with st.expander("📚 Source Citations"):
                                    st.markdown(result["sources"])
                            else:
                                st.info("📚 **Sources:** No specific citations available")
                        
                        else:
                            # Use basic approach
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
                    
                    # Store appropriate data based on what was used
                    if use_confidence and use_sources:
                        st.session_state['chat_history'].append({
                            'question': question,
                            'answer': result["answer"],
                            'confidence': result["confidence"],
                            'sources': result["sources"],
                            'model': model,
                            'type': 'confidence_and_sources'
                        })
                    elif use_confidence:
                        st.session_state['chat_history'].append({
                            'question': question,
                            'answer': result["answer"],
                            'confidence': result["confidence"],
                            'reasoning': result["reasoning"],
                            'model': model,
                            'type': 'confidence'
                        })
                    elif use_sources:
                        st.session_state['chat_history'].append({
                            'question': question,
                            'answer': result["answer"],
                            'sources': result["sources"],
                            'confidence': result["confidence"],
                            'model': model,
                            'type': 'sources'
                        })
                    else:
                        st.session_state['chat_history'].append({
                            'question': question,
                            'answer': answer,
                            'model': model,
                            'type': 'basic'
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
                        
                        # Show additional info based on type
                        if chat.get('type') == 'confidence_and_sources':
                            if chat['confidence'] == "HIGH":
                                st.success(f"✅ **Confidence:** {chat['confidence']}")
                            elif chat['confidence'] == "MEDIUM":
                                st.warning(f"⚠️ **Confidence:** {chat['confidence']}")
                            elif chat['confidence'] == "LOW":
                                st.error(f"❌ **Confidence:** {chat['confidence']}")
                            
                            if chat['sources'] and chat['sources'].lower() != "none":
                                st.markdown("---")
                                st.markdown("**📚 Sources:**")
                                st.markdown(chat['sources'])
                        
                        elif chat.get('type') == 'confidence':
                            if chat['confidence'] == "HIGH":
                                st.success(f"✅ **Confidence:** {chat['confidence']}")
                            elif chat['confidence'] == "MEDIUM":
                                st.warning(f"⚠️ **Confidence:** {chat['confidence']}")
                            elif chat['confidence'] == "LOW":
                                st.error(f"❌ **Confidence:** {chat['confidence']}")
                            st.markdown(f"**Reasoning:** {chat['reasoning']}")
                        
                        elif chat.get('type') == 'sources':
                            if chat['sources'] and chat['sources'].lower() != "none":
                                st.markdown("---")
                                st.markdown("**📚 Sources:**")
                                st.markdown(chat['sources'])
                        
                        st.caption(f"Model: {chat['model']}")
                        
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            st.session_state['chat_history'].pop(-(i+1))
                            st.rerun()

if __name__ == "__main__":
    main() 