# LangChain: Breakfast Idea - Healthy Options

Asks `gpt-4o-mini` (through LangChain's `ChatOpenAI`) for 5 healthy breakfast ideas and prints only the text of the reply.

## Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in this folder (it is git-ignored):

```
OPENAI_API_KEY=your-key
```

Then:

```bash
python breakfast.py          # asks for your ingredients
python breakfast.py --raw    # also shows the full AIMessage object first
```

The script asks:

```
Enter your ingredients separated by commas (or press Enter for 5 healthy breakfast ideas):
```

- Type ingredients (e.g. `oats, banana, milk`) to get at least 3 healthy recipes, each with healthy options.
- Press Enter with nothing to get 5 healthy breakfast ideas.

## Notes

- `llm.invoke()` returns an `AIMessage`, not a string. The text is in `reply.content`.
- `temperature=0` makes runs repeat (close to) the same five ideas. In my two runs the five dishes matched and only small topping details changed.
- The prompt defines "healthy" (high protein or fibre, low added sugar, whole foods, quick) and pins the format (numbered, one line each, no preamble).
- The API key is loaded from `.env` with `python-dotenv`, never hard-coded.
