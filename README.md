# Research Paper Finder with AI Agents

This project is a Streamlit web application that allows users to search for research papers from ArXiv based on a given topic, filter them by publication year, and download the results as a CSV file. It also includes an AI-powered summarization feature using OpenAI's GPT-4.

## Features
- Search research papers on a specific topic from ArXiv.
- Filter results based on a specified publication year range.
- Display research paper details including title, link, summary, first author, and year.
- Summarize research papers using OpenAI's GPT-4.
- Download research paper details as a CSV file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/roshni123-source/Research-Paper-finder.git
   cd Research-Paper-finder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Open the `app.py` file and replace `Your_Api_key` with your actual OpenAI API key.
   - Alternatively, set the API key as an environment variable:
     ```bash
     export OPENAI_API_KEY='your_api_key'
     ```
          
## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```

## How It Works
1. The user enters a research topic in the input field.
2. The application fetches research papers from ArXiv based on the search query and filters them by year.
3. The results are displayed with the title, author, publication year, summary, and a link to the full paper.
4. Users can download the search results as a CSV file.

