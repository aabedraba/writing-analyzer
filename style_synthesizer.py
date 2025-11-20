import asyncio
from typing import List
from agno.agent import Agent, RunOutput
from agno.team import Team
from article_analyzer import article_analyzer, fetch_article_content


style_synthesizer = Team(
    members=[article_analyzer],
    name="Writing Style Synthesizer",
    instructions="""You are an expert at identifying patterns in writing style across multiple pieces of content.

When given analyses from multiple articles by the same author, your task is to:

1. Identify patterns that appear across MULTIPLE articles (not just one)
2. Highlight the most distinctive and consistent characteristics
3. Determine what truly stands out as unique to this author
4. Define the core elements of their voice and approach

Do NOT simply summarize each individual analysis. Instead, identify the common threads and most salient features that define this author's style across their body of work.

Provide a concise, synthesized description of the author's writing style (3-5 paragraphs maximum). Focus on what consistently stands out and makes their voice unique.""",
    model="anthropic:claude-sonnet-4-5-20250929",
    markdown=True,
)


async def analyze_articles(urls: List[str]) -> dict:
    """
    Coordinate analysis of multiple articles in parallel.

    Returns a dict with:
    - individual_analyses: list of analyses from sub-agents
    - synthesized_style: final synthesized writing style description
    - errors: list of any errors that occurred
    """
    print(f"Starting analysis of {len(urls)} articles...")

    # Fetch all articles in parallel
    async def fetch_and_analyze(url: str) -> dict:
        try:
            content = await fetch_article_content(url)

            # Run the article analyzer agent
            response: RunOutput = article_analyzer.run(
                f"Analyze the writing style of this article:\n\n{content}"
            )

            return {
                "url": url,
                "style_analysis": response.content,
            }
        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "style_analysis": None,
            }

    # Execute all sub-agents in parallel
    individual_analyses = await asyncio.gather(
        *[fetch_and_analyze(url) for url in urls]
    )

    # Separate successful analyses from errors
    successful_analyses = [
        a for a in individual_analyses if a.get("style_analysis")
    ]
    errors = [
        {"url": a["url"], "error": a["error"]}
        for a in individual_analyses
        if a.get("error")
    ]

    print(f"Completed {len(successful_analyses)} successful analyses")
    if errors:
        print(f"Encountered {len(errors)} errors")

    # Synthesize the results using the main agent
    if successful_analyses:
        print("Synthesizing writing style from all analyses...")

        analyses_text = "\n\n".join([
            f"Article {i+1} ({analysis['url']}):\n{analysis['style_analysis']}"
            for i, analysis in enumerate(successful_analyses)
        ])

        synthesis_response: RunOutput = style_synthesizer.run(
            f"Here are the individual writing style analyses:\n\n{analyses_text}\n\nProvide a synthesized description of the author's overall writing style."
        )

        synthesized_style = synthesis_response.content
    else:
        synthesized_style = "Could not synthesize style due to lack of successful analyses."

    return {
        "individual_analyses": individual_analyses,
        "synthesized_style": synthesized_style,
        "errors": errors,
    }
