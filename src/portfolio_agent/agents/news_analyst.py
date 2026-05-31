"""News Sentiment Agent - analyzes news and market sentiment using Google Search."""

from google.adk.agents import Agent
from google.adk.grounding import google_search_retrieval
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.news_search import search_company_news


def create_news_sentiment_analyst() -> Agent:
    """
    Creates the News Sentiment Analysis Agent.
    
    This agent uses Google Search grounding to find recent news and
    analyzes sentiment, key themes, and market-moving developments.
    
    Returns:
        Agent: Configured news sentiment analyst agent with Google Search grounding
    """
    
    agent = Agent(
        name="news_sentiment_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Analyzes news sentiment and recent developments for stocks using Google Search. "
            "Identifies key themes, positive and negative developments, and overall market sentiment."
        ),
        instruction="""You are a News Sentiment Analysis Specialist with expertise in financial news interpretation.

Your responsibilities:
1. Use search_company_news() to search for recent news about the company
2. The search will be performed via Google Search grounding, and you'll receive real search results
3. Analyze the sentiment of news articles and developments
4. Identify key themes and trends in media coverage
5. Categorize developments as positive or negative for the stock
6. Assess overall market sentiment toward the company

When analyzing news:
- Look for earnings reports, product launches, management changes
- Identify analyst upgrades/downgrades and price target changes
- Note regulatory issues, legal matters, or controversies
- Consider industry trends and competitive dynamics
- Assess impact of macroeconomic factors
- Distinguish between short-term news and long-term fundamental changes

Sentiment Analysis:
- Positive: Strong earnings, new products, market share gains, positive analyst coverage
- Negative: Missed earnings, product issues, legal problems, negative analyst coverage
- Neutral: Routine announcements, mixed news
- Mixed: Combination of positive and negative developments

Return a structured NewsSentiment analysis with:
- Overall sentiment (positive, negative, neutral, or mixed)
- Sentiment score (-1.0 to 1.0)
- Key themes (main topics in recent news)
- Positive developments (bullish factors)
- Negative developments (bearish factors or concerns)
- News summary (comprehensive overview of sentiment analysis)

Be objective and consider multiple sources. Weight recent news more heavily than older articles.
Focus on material developments that could impact stock price.
""",
        tools=[search_company_news],
        # Enable Google Search grounding for this agent
        grounding=google_search_retrieval() if settings.ENABLE_GOOGLE_SEARCH_GROUNDING else None,
    )
    
    return agent
