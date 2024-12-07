import json

class HighScores:
    def __init__(self, filename='high_scores.json'):
        self.filename = filename
        self.scores = self.load_high_scores()

    def load_high_scores(self):
        """Load high scores from a file."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return an empty list if file not found
            return [0] * 10

    def save_high_scores(self):
        """Save high scores to a file."""
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)

    def update_high_scores(self, new_score):
        """Add new score to the high scores if it's in the top 10."""
        self.scores.append(new_score)
        self.scores = sorted(self.scores, reverse=True)[:10]  # Keep only top 10
        self.save_high_scores()
