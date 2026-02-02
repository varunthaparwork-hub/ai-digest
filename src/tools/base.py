from typing import List, Dict

class SourceAdapter:
    def fetch_items(self, hours: int = 24) -> List[Dict]:
        raise NotImplementedError
