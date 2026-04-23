import asyncio
from app.crawler import crawl_website
from app.processor import structure_content
from app.llm import analyze_content
from app.cache import save_to_cache

def process_website(url: str):
    print(f"STARTING ANALYSIS: {url} ")
    
    #  URL Normalization
    if not url.startswith("http"):
        url = "https://" + url

    try:
        # Run the async crawler
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(crawl_website(url))

        # Structure the results
        structured_data = structure_content(results)
        
        full_site_analysis = []

        # 4. Process each page
        for item in structured_data:
            page_url = item['page']
            content = item['content']
            
            print(f"Analyzing {page_url}...")

            # Empty Page Guard
            if not content or len(content.strip()) < 50:
                print(f"Guard Triggered: Low content detected for {page_url}")
                analysis_output = {
                    "scores": {"professionalism": 0, "urgency": 0, "clarity": 0, "trust": 0},
                    "improvements": [],
                    "gaps": [
                        {
                            "missing": "Textual Content",
                            "location": "Main Body",
                            "outline": "Add descriptive text about your services or mission.",
                            "reason": "The page is currently empty or has very little text."
                        }
                    ]
                }
            else:
                # Normal path: Send to LLM (Now returns scores + audit)
                analysis_output = analyze_content(page_url, content)

            full_site_analysis.append({
                "page": page_url,
                "results": analysis_output
            })

        # AGGREGATE SITE-WIDE BRAND HEALTH SUMMARY 
        total_pages = len(full_site_analysis)
        site_health = {"professionalism": 0, "urgency": 0, "clarity": 0, "trust": 0}

        if total_pages > 0:
            for page in full_site_analysis:
                # Extract scores from the LLM output (defaults to 5 if model fails to score)
                page_scores = page["results"].get("scores", {})
                for metric in site_health:
                    site_health[metric] += page_scores.get(metric, 5)

            # Calculate the average and round to 1 decimal place
            for metric in site_health:
                site_health[metric] = round(site_health[metric] / total_pages, 1)

        # Save final result to SQLite Cache with the new Scorecard
        final_payload = {
            "status": "Completed", 
            "site_health_summary": site_health,
            "report": full_site_analysis
        }
        
        save_to_cache(url, final_payload)
        print(f"ANALYSIS & SITE-WIDE SCORES SAVED FOR {url} ")

    except Exception as e:
        # Handling edge cases: Inaccessible pages or crawl failures
        error_report = {"status": "Failed", "error": f"Task error: {str(e)}"}
        save_to_cache(url, error_report)
        print(f" Error processing {url}: {e}")