"""News Sentiment Agent - analyzes news and market sentiment using Google Search."""

import logging
from google.adk.agents import Agent, google_search
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.news_search import search_company_news
from portfolio_agent.prompts.loader import load_prompt


def create_news_sentiment_analyst() -> Agent:
    """
    Creates the News Sentiment Analysis Agent.
    
    This agent uses Google Search grounding to find recent news and
    analyzes sentiment, key themes, and market-moving developments.
    
    Returns:
        Agent: Configured news sentiment analyst agent with Google Search grounding
    """
    
    instruction = load_prompt("news_analyst.jinja")
    
    agent = Agent(
        name="news_sentiment_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Analyzes news sentiment and recent developments for stocks using Google Search. "
            "Identifies key themes, positive and negative developments, and overall market sentiment."
        ),
        instruction=instruction,
        tools=[search_company_news],
        # Enable Google Search grounding for this agent
        grounding=google_search() if settings.ENABLE_GOOGLE_SEARCH_GROUNDING else None,
    )
    
    return agent
