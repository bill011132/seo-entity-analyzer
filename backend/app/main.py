from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.serper import search_google
from app.services.scraper import fetch_article_text
from app.services.nlp import extract_entities, group_entities_by_topic
from app.services.sheets import write_to_google_sheet


app = FastAPI(
    title="SEO Entity Analyzer API",
    description="Analyze Google search results and extract SEO entities.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "SEO Entity Analyzer API is running."
    }


@app.get("/api/search")
def search(keyword: str = Query(..., description="Search keyword")):
    """
    Search Google first page results by keyword.
    """

    try:
        results = search_google(keyword=keyword, num_results=10)

        return {
            "keyword": keyword,
            "count": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analyze")
def analyze(keyword: str = Query(..., description="Search keyword")):
    """
    Search Google first page results, fetch each article,
    and count entities for each article.
    """

    try:
        search_results = search_google(keyword=keyword, num_results=10)

        analyzed_results = []

        for item in search_results:
            url = item.get("link", "")

            article_text = fetch_article_text(url)
            entity_result = extract_entities(article_text, top_k=30)

            analyzed_results.append({
                "rank": item.get("rank"),
                "title": item.get("title"),
                "url": url,
                "snippet": item.get("snippet"),
                "text_length": len(article_text),
                "entity_total_count": entity_result["entity_total_count"],
                "unique_entity_count": entity_result["unique_entity_count"],
                "entities": entity_result["entities"],
            })

        return {
            "keyword": keyword,
            "result_count": len(analyzed_results),
            "results": analyzed_results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/analyze-with-topics")
def analyze_with_topics(keyword: str = Query(..., description="Search keyword")):
    """
    Search Google first page results, extract entities,
    and group entities into topic clusters.
    """

    try:
        search_results = search_google(keyword=keyword, num_results=10)

        analyzed_results = []

        for item in search_results:
            url = item.get("link", "")

            article_text = fetch_article_text(url)
            entity_result = extract_entities(article_text, top_k=30)

            analyzed_results.append({
                "rank": item.get("rank"),
                "title": item.get("title"),
                "url": url,
                "snippet": item.get("snippet"),
                "text_length": len(article_text),
                "entity_total_count": entity_result["entity_total_count"],
                "unique_entity_count": entity_result["unique_entity_count"],
                "entities": entity_result["entities"],
            })

        topic_groups = group_entities_by_topic(analyzed_results)

        return {
            "keyword": keyword,
            "result_count": len(analyzed_results),
            "articles": analyzed_results,
            "topic_groups": topic_groups,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/analyze-and-export")
def analyze_and_export(keyword: str = Query(..., description="Search keyword")):
    """
    Search Google first page results, extract entities,
    group entities by topics, and export results to Google Sheet.
    """

    try:
        search_results = search_google(keyword=keyword, num_results=10)

        analyzed_results = []

        for item in search_results:
            url = item.get("link", "")

            article_text = fetch_article_text(url)
            entity_result = extract_entities(article_text, top_k=30)

            analyzed_results.append({
                "rank": item.get("rank"),
                "title": item.get("title"),
                "url": url,
                "snippet": item.get("snippet"),
                "text_length": len(article_text),
                "entity_total_count": entity_result["entity_total_count"],
                "unique_entity_count": entity_result["unique_entity_count"],
                "entities": entity_result["entities"],
            })

        topic_groups = group_entities_by_topic(analyzed_results)

        payload = {
            "keyword": keyword,
            "result_count": len(analyzed_results),
            "articles": analyzed_results,
            "topic_groups": topic_groups,
        }

        sheet_result = write_to_google_sheet(payload)

        return {
            "message": "Analysis completed and exported to Google Sheet.",
            "keyword": keyword,
            "result_count": len(analyzed_results),
            "sheet_result": sheet_result,
            "articles": analyzed_results,
            "topic_groups": topic_groups,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))