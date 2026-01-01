"""Bot configuration and data storage."""
import json
import os
from typing import List, Tuple, Set
from pathlib import Path


class BotConfig:
    """Manages bot configuration and persistent data."""

    def __init__(self, config_file: str = "bot_data.json"):
        self.config_file = config_file
        self.data = self._load_data()

    def _load_data(self) -> dict:
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                "wanted_combinations": [
                    ["Ionic Dryer", "Love Burst"],
                    ["Spring Basket", "Ritual Goat"],
                    ["Jolly Chimp", "La Baboon"]
                ],
                "max_price": 31,
                "check_interval_minutes": 10,
                "monitoring_enabled": True,
                "seen_gift_ids": [],
                "statistics": {
                    "total_checks": 0,
                    "total_new_gifts_found": 0,
                    "last_check_time": None
                }
            }

    def save(self):
        """Save configuration to JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    # Wanted combinations management
    def get_wanted_combinations(self) -> List[Tuple[str, str]]:
        """Get list of wanted gift+model combinations."""
        return [tuple(c) for c in self.data["wanted_combinations"]]

    def add_combination(self, gift_name: str, model: str) -> bool:
        """Add a new gift+model combination."""
        combo = [gift_name, model]
        if combo not in self.data["wanted_combinations"]:
            self.data["wanted_combinations"].append(combo)
            self.save()
            return True
        return False

    def remove_combination(self, gift_name: str, model: str) -> bool:
        """Remove a gift+model combination."""
        combo = [gift_name, model]
        if combo in self.data["wanted_combinations"]:
            self.data["wanted_combinations"].remove(combo)
            self.save()
            return True
        return False

    # Price management
    def get_max_price(self) -> int:
        """Get maximum price filter."""
        return self.data["max_price"]

    def set_max_price(self, price: int):
        """Set maximum price filter."""
        self.data["max_price"] = price
        self.save()

    # Interval management
    def get_check_interval(self) -> int:
        """Get check interval in minutes."""
        return self.data["check_interval_minutes"]

    def set_check_interval(self, minutes: int):
        """Set check interval in minutes."""
        self.data["check_interval_minutes"] = minutes
        self.save()

    # Monitoring control
    def is_monitoring_enabled(self) -> bool:
        """Check if monitoring is enabled."""
        return self.data["monitoring_enabled"]

    def set_monitoring_enabled(self, enabled: bool):
        """Enable or disable monitoring."""
        self.data["monitoring_enabled"] = enabled
        self.save()

    # Seen gifts tracking
    def get_seen_gift_ids(self) -> Set[str]:
        """Get set of already seen gift IDs."""
        return set(self.data["seen_gift_ids"])

    def mark_gifts_as_seen(self, gift_ids: List[str]):
        """Mark gifts as seen."""
        seen = set(self.data["seen_gift_ids"])
        seen.update(gift_ids)
        # Keep only last 1000 IDs to avoid infinite growth
        self.data["seen_gift_ids"] = list(seen)[-1000:]
        self.save()

    def clear_seen_gifts(self):
        """Clear all seen gifts (useful for testing)."""
        self.data["seen_gift_ids"] = []
        self.save()

    # Statistics
    def increment_check_count(self):
        """Increment total check counter."""
        self.data["statistics"]["total_checks"] += 1
        self.save()

    def add_new_gifts_found(self, count: int):
        """Add to total new gifts found."""
        self.data["statistics"]["total_new_gifts_found"] += count
        self.save()

    def update_last_check_time(self, timestamp: str):
        """Update last check timestamp."""
        self.data["statistics"]["last_check_time"] = timestamp
        self.save()

    def get_statistics(self) -> dict:
        """Get statistics."""
        return self.data["statistics"]
