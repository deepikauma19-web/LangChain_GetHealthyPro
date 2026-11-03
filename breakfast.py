"""
breakfast.py

Usage:
    python breakfast.py          # asks for your ingredients
    python breakfast.py --raw    # also prints the full message object first

Type ingredients (e.g. oats, banana, milk) to get at least 3 healthy recipes, each with healthy options,
or press Enter with nothing to get 5 healthy breakfast ideas.

The API key is read from OPENAI_API_KEY in the .env file.
"""

import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load OPENAI_API_KEY from the .env file into the environment
load_dotenv()

# Define "healthy" ourselves instead of letting the model decide
HEALTHY = (
    "Healthy means: high in protein or fibre, low in added sugar, "
    "made from whole foods, and quick to prepare at home."
)


def ideas_prompt() -> str:
    # Pin the output format so there is no preamble or extra text.
    return (
        f"Give me exactly 5 healthy breakfast ideas. {HEALTHY}\n"
        "Format rules:\n"
        "- A numbered list from 1 to 5.\n"
        "- One line per idea, the dish name plus a few words on what is in it.\n"
        "- No introduction, no closing sentence, nothing else."
    )


def recipe_prompt(ingredients: str) -> str:
    return (
        f"I have these ingredients: {ingredients}.\n"
        "Suggest at least 3 different healthy breakfast recipes that use them. "
        f"{HEALTHY}\n"
        "Each recipe must be a different dish, not a variation of another. "
        "You may add common pantry items (salt, spices, oil, water), and list "
        "any other extra item as optional.\n"
        "Format rules, repeat these sections for every recipe and add nothing else:\n"
        "Recipe <number>: <dish name>\n"
        "Ingredients:\n"
        "- <item with quantity>\n"
        "Steps:\n"
        "1. <step>\n"
        "Healthy options:\n"
        "- <swap or addition that makes it healthier, and why in a few words>\n"
        "Give 2 to 3 healthy options per recipe. Put a blank line between recipes. "
        "No introduction, no closing sentence."
    )


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Add OPENAI_API_KEY=your-key to the .env file")

    # Ask the user for their ingredients; pressing Enter with nothing gives 5 ideas
    ingredients = input(
        "Enter your ingredients separated by commas "
        "(or press Enter for 5 healthy breakfast ideas): "
    ).strip()
    print()

    # temperature=0 makes the model pick its most likely answer each time,
    # so repeated runs give (nearly) the same output.
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = recipe_prompt(ingredients) if ingredients else ideas_prompt()
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
