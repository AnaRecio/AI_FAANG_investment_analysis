from crewai_tools import SerperDevTool
from typing import List, Dict
import re

# Instantiate the Serper search tool (uses Serper.dev with env-based API key)
serper_search = SerperDevTool()

def clean_snippet(text: str) -> str:
    """
    Cleans a snippet by removing extra whitespace and line breaks.
    Useful for compact formatting in summaries.
    """
    return re.sub(r'\s+', ' ', text.strip())

def extract_company_info(company_name: str, query_suffix: str = "Q1 2025 performance stock forecast", max_results: int = 5) -> Dict:
    """
    Performs a Serper search for a specific company using a stock-focused query,
    and returns structured summary data and sources.
    
    Args:
        company_name (str): Name of the FAANG company.
        query_suffix (str): Tail of the search query to focus on performance and forecast.
        max_results (int): Max number of search results to include in summary.

    Returns:
        dict: {
            "company": company name,
            "summary": concatenated text of snippets,
            "sources": list of source {title, url} objects
        }
    """
    query = f"{company_name} {query_suffix}"
    raw_results = serper_search.run(query)

    # Handle edge case where Serper returns a string error or fallback
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

        # Include result only if both snippet and link are present
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
    Iterates through a list of companies and gathers structured web research data
    using extract_company_info for each one.

    Args:
        companies (List[str]): List of company names to search.

    Returns:
        List[Dict]: List of structured company info dicts.
    """
    all_data = []
    for company in companies:
        print(f"🔍 Searching data for: {company}")
        company_info = extract_company_info(company)
        all_data.append(company_info)
    return all_data
