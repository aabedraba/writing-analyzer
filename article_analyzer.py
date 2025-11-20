import httpx
from agno.agent import Agent


async def fetch_article_content(url: str) -> str:
    """Fetch the article content from the URL."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


article_analyzer = Agent(
    name="Article Style Analyzer",
    instructions="""You are an expert at analyzing writing style for technical articles.

Be concise but specific. Provide a clear, actionable description of the writing style in 2-4 paragraphs maximum.

Focus on what makes this writing distinctive and memorable.""",
    model="anthropic:claude-sonnet-4-5-20250929",
)
