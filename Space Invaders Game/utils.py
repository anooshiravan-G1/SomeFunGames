import json
import os


def load_high_score():
    """Load high score from JSON file."""
    try:
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
    except Exception as e:
        print(f"Error loading high score: {e}")
    return 0


def save_high_score(score):
    """Save high score to JSON file."""
    try:
        with open("high_score.json", "w") as f:
            json.dump({"high_score": score}, f)
    except Exception as e:
        print(f"Error saving high score: {e}")
