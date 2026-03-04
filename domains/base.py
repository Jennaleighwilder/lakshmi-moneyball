"""
Base domain fetcher — all 12 domains extend this.
Returns: list of {domain, ticker, title, price, edge_signal, raw}
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any


class DomainFetcher(ABC):
    domain: str = "base"

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch live data. Return list of opportunities."""
        pass

    def to_record(self, item: Dict) -> Dict:
        """Standard record for history/learning."""
        return {
            "domain": self.domain,
            "ts": datetime.now().isoformat(),
            "data": item,
        }
