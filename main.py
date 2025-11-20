import asyncio
from style_synthesizer import analyze_articles


# Add your article URLs here
ARTICLE_URLS = [
  "https://langfuse.com/blog/2025-11-12-evals.md",
  "https://langfuse.com/guides/cookbook/example_simulated_multi_turn_conversations.md",
  "https://langfuse.com/blog/2025-10-28-rag-observability-and-evals.md",
  "https://langfuse.com/blog/2025-10-21-testing-llm-applications.md",
  "https://langfuse.com/blog/2025-10-09-evaluating-multi-turn-conversations.md",
]

async def run_analysis():
    """Run the multi-agent writing style analysis using Agno."""
    print(f"Analyzing writing style from {len(ARTICLE_URLS)} articles using Agno multi-agent system...")
    print("This may take a moment as we fetch and analyze each article.\n")

    results = await analyze_articles(ARTICLE_URLS)

    # Display results
    print("\n" + "=" * 80)
    print("WRITING STYLE ANALYSIS RESULTS")
    print("=" * 80 + "\n")

    # Show any errors
    if results["errors"]:
        print("ERRORS:")
        for error in results["errors"]:
            print(f"  - {error['url']}: {error['error']}")
        print()

    # Show synthesized style
    print("SYNTHESIZED WRITING STYLE:")
    print("-" * 80)
    print(results["synthesized_style"])
    print("-" * 80 + "\n")

    return results


if __name__ == "__main__":
    asyncio.run(run_analysis())
