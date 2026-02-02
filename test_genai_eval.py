import json
import sqlite3
from tools.genai_news_evaluator import evaluate_item
from services.storage import insert_evaluation

conn = sqlite3.connect('data/digest.db')
cur = conn.cursor()

cur.execute('SELECT id, title FROM items LIMIT 1')
row = cur.fetchone()

if not row:
    print('No items found')
    exit()

item_id, title = row

item = {'title': title}
result = evaluate_item(item)

if result:
    insert_evaluation(
        item_id=item_id,
        persona='GENAI_NEWS',
        score=result['relevance_score'],
        decision=result['decision'],
        json_data=json.dumps(result)
    )
    print('Evaluation stored:', result)
else:
    print('Evaluation failed')

conn.close()
