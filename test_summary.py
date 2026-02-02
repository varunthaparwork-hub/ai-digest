from workflows.genai_selector import load_relevant_items
from workflows.genai_summarizer import summarize_item

items = load_relevant_items()

if items:
    _, title, content, _ = items[0]
    summary = summarize_item(title, content)
    print(summary)
else:
    print('No items to summarize')
