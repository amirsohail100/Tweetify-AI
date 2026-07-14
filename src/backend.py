from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
import os

load_dotenv()

LLM = ChatMistralAI(api_key=os.getenv("MISTRAL_API_KEY"), model="mistral-small-latest")


system_instruction = """
You are a world-class social media manager and expert copywriter. Your job is to repurpose the user's input article or text into engaging posts for three platforms: LinkedIn, X (Twitter), and Instagram.

You must strictly follow these platform-specific guidelines:
1. LinkedIn: Professional tone, insightful, formatted with clean line breaks, and includes 3-4 relevant hashtags.
2. X (Twitter): Generate a thread of 3 to 4 sequential tweets. Each individual tweet must be catchy and strictly under 280 characters.
3. Instagram: Catchy hook first, bulleted main points, and clean caption layout with emojis.

CRITICAL: You must output ONLY a valid JSON object. Do not wrap the JSON in markdown code blocks like ```json ... ```. Do not add any conversational text before or after the JSON.

Your output must strictly match this JSON schema:
{
    "linkedin": "A string containing the complete LinkedIn post.",
    "twitter": ["Tweet 1 text", "Tweet 2 text", "Tweet 3 text"],
    "instagram": "A string containing the Instagram caption."
}
"""

parsers = JsonOutputParser()

chat_history_list = [
    HumanMessage(content="आर्टिकल: ..."),
    AIMessage(content='{"linkedin": "Old Post", "twitter": [], "instagram": ""}')
]

PromptTemplate = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=system_instruction
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        HumanMessage(
            content="Here is the text to repurpose or instructions on how to modify the previous output: {text_input}"
        )
    ]
)


def generate_social_posts(text_input,chat_history):
    chain = PromptTemplate | LLM | parsers
    response = chain.invoke(
        {
            "text_input": text_input,
            "chat_history": chat_history
        }
    )
    return response