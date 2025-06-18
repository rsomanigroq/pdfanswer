# PDF Question Answering with Groq

A simple Streamlit application that uses Groq's LLM API to answer questions based on PDF files. Upload any PDF document and ask questions about its content using powerful language models with **advanced hallucination prevention**.

## Features

- 📄 **PDF Upload**: Upload and extract text from PDF files
- 🤖 **AI-Powered Q&A**: Ask questions using Groq's LLM models
- 🎯 **Multiple Models**: Choose from different Groq models (Llama, Mixtral, Gemma)
- 💬 **Chat History**: Keep track of your questions and answers
- 🎨 **Modern UI**: Clean and intuitive Streamlit interface
- 🛡️ **Hallucination Prevention**: Advanced features to detect and prevent AI hallucinations

## 🛡️ Hallucination Prevention Features

### Confidence Scoring
- **Self-Assessment**: LLM rates its own confidence in answers (HIGH/MEDIUM/LOW)
- **Reasoning**: Provides explanation for confidence level
- **Visual Indicators**: Color-coded confidence levels in the UI

### Source Citations
- **Exact Quotes**: Shows specific text that supports the answer
- **Verification**: Users can verify answers against source material
- **Transparency**: Clear indication when information is not found

### Smart Detection
- **Low Confidence Warnings**: Alerts when LLM is uncertain
- **Missing Information**: Properly handles questions about non-existent content
- **Consistent Responses**: Multiple verification approaches

## Supported Models

- `llama3-8b-8192` (default) - Fast and efficient
- `llama3-70b-8192` - More powerful, larger model
- `mixtral-8x7b-32768` - Excellent performance
- `gemma2-9b-it` - Google's Gemma model

## Setup

### 1. Clone and Navigate
```bash
cd /Users/rsomani/pdf_infosec
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Groq API Key

#### Option A: Environment Variable
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

#### Option B: Create .env File
```bash
cp env_example.txt .env
# Edit .env file and add your API key
```

### 5. Get Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your environment

## Usage

### Start the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### How to Use
1. **Upload PDF**: Click "Browse files" and select a PDF document
2. **Wait for Processing**: The app will extract text from your PDF
3. **Configure Settings**: Choose hallucination prevention options in the sidebar
4. **Ask Questions**: Type your question in the text area
5. **Review Results**: Get AI-powered answers with confidence scores and source citations
6. **Check History**: Review previous questions and answers with confidence levels

### Hallucination Prevention Settings

In the sidebar, you can enable/disable:
- ✅ **Show confidence scores**: LLM rates its own confidence
- ✅ **Show source citations**: Display exact supporting text

## Example Questions

- "What is the main topic of this document?"
- "Summarize the key points in the first chapter"
- "What are the conclusions mentioned in the document?"
- "List all the important dates mentioned"
- "What methodology was used in this research?"

## Testing Hallucination Prevention

Run the test script to verify all features work correctly:
```bash
python test_hallucination_prevention.py
```

This will test:
- Confidence scoring functionality
- Source citation accuracy
- Hallucination detection with non-existent information

## Project Structure

```
pdf_infosec/
├── app.py                           # Main Streamlit application with hallucination prevention
├── test_hallucination_prevention.py # Test script for hallucination features
├── requirements.txt                 # Python dependencies
├── env_example.txt                  # Environment variables template
├── README.md                       # This file
└── venv/                           # Virtual environment
```

## Dependencies

- **Streamlit**: Web application framework
- **Groq**: Python client for Groq API
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management
- **LangChain**: (Optional) For advanced LLM features

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GROQ_API_KEY` is set correctly
2. **PDF Reading Error**: Ensure the PDF is not corrupted or password-protected
3. **Import Errors**: Make sure all dependencies are installed in your virtual environment
4. **Low Confidence**: This is expected for questions about non-existent information

### Getting Help

- Check the [Groq API Documentation](https://console.groq.com/docs)
- Review [Streamlit Documentation](https://docs.streamlit.io/)
- Ensure your virtual environment is activated

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 