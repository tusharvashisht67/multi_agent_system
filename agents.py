from pathlib import Path
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url


# Load .env explicitly
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

gemini_key = os.getenv("GEMINI_API_KEY")

print("GEMINI KEY LOADED:", bool(gemini_key))

if not gemini_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please add it in your .env file.")


# Model setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0
)


# 1st agent - Search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# 2nd agent - Reader agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()