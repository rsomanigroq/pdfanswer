# PDF Question Answering with Groq

A simple Streamlit application that uses Groq's LLM API to answer questions based on PDF files. Upload any PDF document and ask questions about its content using powerful language models.

## Features

- 📄 **PDF Upload**: Upload and extract text from PDF files
- 🤖 **AI-Powered Q&A**: Ask questions using Groq's LLM models
- 🎯 **Multiple Models**: Choose from different Groq models (Llama, Mixtral, Gemma)
- 💬 **Chat History**: Keep track of your questions and answers
- 🎨 **Modern UI**: Clean and intuitive Streamlit interface

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
3. **Ask Questions**: Type your question in the text area
4. **Get Answers**: Click "Ask Groq" to get AI-powered answers
5. **Review History**: Check your previous questions and answers

## Example Questions

- "What is the main topic of this document?"
- "Summarize the key points in the first chapter"
- "What are the conclusions mentioned in the document?"
- "List all the important dates mentioned"
- "What methodology was used in this research?"

## Project Structure

```
pdf_infosec/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
├── README.md          # This file
└── venv/              # Virtual environment
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

### Getting Help

- Check the [Groq API Documentation](https://console.groq.com/docs)
- Review [Streamlit Documentation](https://docs.streamlit.io/)
- Ensure your virtual environment is activated

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 