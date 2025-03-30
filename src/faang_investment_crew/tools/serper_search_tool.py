from crewai_tools import SerperDevTool
from typing import List, Dict
import re

# Instantiate the Serper tool (no API key needed if using env vars)
serper_search = SerperDevTool()

def clean_snippet(text: str) -> str:
    """
    Clean snippet by removing line breaks and extra spaces.
    """
    return re.sub(r'\s+', ' ', text.strip())

def extract_company_info(company_name: str, query_suffix: str = "Q1 2025 performance stock forecast", max_results: int = 5) -> Dict:
    """
    Perform Serper search and extract structured results for a given FAANG company.
    """
    query = f"{company_name} {query_suffix}"
    raw_results = serper_search.run(query)

    if isinstance(raw_results, str):
        return {
            "company": company_name,
            "summary": raw_results,
            "sources": []
        }

    snippets = []
    sources = []

    organic_results = raw_results.get("organic", [])

    for result in organic_results[:max_results]:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")

        if snippet and link:
            snippets.append(f"**{title}**: {clean_snippet(snippet)}")
            sources.append({"title": title, "url": link})

    return {
        "company": company_name,
        "summary": "\n".join(snippets),
        "sources": sources
    }

def fetch_faang_company_data(companies: List[str]) -> List[Dict]:
    """
    Fetch research data for multiple companies using Serper.
    """
    all_data = []
    for company in companies:
        print(f"🔍 Searching data for: {company}")
        company_info = extract_company_info(company)
        all_data.append(company_info)
    return all_data
