# Import all dependencies
import requests
import feedparser
import csv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = "Your_Api_key"

# Initialize LLM Model
llm = ChatOpenAI(model_name="gpt-4")

# Method to fetch papers from ArXiv
def search_papers(query, max_results=10, start_year=2010, end_year=2025):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    if response.status_code == 200:
        feed = feedparser.parse(response.text)
        papers = []
        for entry in feed.entries:
            year = entry.published[:4] if 'published' in entry else "Unknown"
            if year.isdigit() and (int(year) < start_year or int(year) > end_year):
                continue  
            paper_info = {
                "Title": entry.title,
                "Link": entry.link,
                "Summary": entry.summary[:300] + "..." if len(entry.summary) > 300 else entry.summary,
                "First Author": entry.authors[0] if entry.authors else "Unknown",
                "Year": year
            }
            papers.append(paper_info)
        return papers
    else:
        return []

# Summarization Chain
template_summary = PromptTemplate(
    input_variables=["paper_content"],
    template="Summarize this research paper: {paper_content} in 3-4 sentences."
)
summarization_chain = LLMChain(llm=llm, prompt=template_summary)
def summarize_paper(content):
    return summarization_chain.run(content)

# Streamlit App
st.title("Research Paper Finder with AI Agents")
# User Inputs 
query = st.text_input("Enter a research topic:", placeholder="Brain Tumor Detection")
num_papers = st.number_input("Number of papers to retrieve:", min_value=1, max_value=50, value=10)
# Year selection slider (2025 to 2010)
start_year, end_year = st.slider("Select publication year range:", 2010, 2025, (2015, 2025))
if st.button("Search Papers"):
    if query:
        papers = search_papers(query, num_papers, start_year, end_year)
        if papers:
            st.success(f"Found {len(papers)} papers on '{query}' published between {start_year} and {end_year}.")
            for i, paper in enumerate(papers, start=1):
                with st.expander(f"Paper {i}: {paper['Title']}"):
                    st.markdown(f"**[Link to Paper]({paper['Link']})**")
                    st.markdown(f" **Summary:** {paper['Summary']}")
                    st.markdown(f"**First Author:** {paper['First Author']}")
                    st.markdown(f"**Year:** {paper['Year']}")
            # Save papers to CSV
            def save_to_csv(papers):
                keys = ["Title", "Link", "Summary", "First Author", "Year"]
                filename = "papers.csv"
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(papers)
                return filename
            # Provide CSV download option
            csv_filename = save_to_csv(papers)
            with open(csv_filename, "rb") as file:
                st.download_button(label="Download CSV", data=file, file_name=csv_filename, mime="text/csv")
        else:
            st.warning(f"No papers found for the given topic in the selected year range ({start_year} - {end_year}).")
    else:
        st.error("Please enter a research topic.")

