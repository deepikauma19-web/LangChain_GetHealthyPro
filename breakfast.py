"""
breakfast.py

Week 2 Day 5: ask LangChain for 5 healthy breakfast ideas and print them.

Usage:
    python breakfast.py          # prints the 5 ideas
    python breakfast.py --raw    # also prints the full message object first

The API key is read from OPENAI_API_KEY in the .env file.
"""

import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load OPENAI_API_KEY from the .env file into the environment
load_dotenv()


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Add OPENAI_API_KEY=your-key to the .env file")

    # temperature=0 makes the model pick its most likely answer each time,
    # so repeated runs give (nearly) the same five ideas.
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define "healthy" ourselves instead of letting the model decide,
    # and pin the output format so there is no preamble or extra text.
    prompt = (
        "Give me exactly 5 healthy breakfast ideas. "
        "Healthy means: high in protein or fibre, low in added sugar, "
        "made from whole foods, and quick to prepare at home.\n"
        "Format rules:\n"
        "- A numbered list from 1 to 5.\n"
        "- One line per idea, the dish name plus a few words on what is in it.\n"
        "- No introduction, no closing sentence, nothing else."
    )

    reply = llm.invoke(prompt)

    if "--raw" in sys.argv:
        # invoke() returns an AIMessage object, not a string.
        print("Raw reply object:")
        print(reply)
        print()

    # The text we actually want lives in .content
    print(reply.content)


if __name__ == "__main__":
    main()
