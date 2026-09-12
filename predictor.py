import random

class RacePredictor:
    def __init__(self):
        self.model_version = "CardPredictor-v1.0"

    def calculate_probabilities(self, runners):
        """
        Computes percentage-based win probabilities based on form, weight, and rating.
        """
        total_score = 0                                                 scored_runners = []

        for r in runners:
            # Weighted calculation
            form = r.get("form", 50)
            rating = r.get("rating", 50)
            raw_score = (rating * 0.5) + (form * 0.4) + random.uniform(1, 5)
            total_score += raw_score
            scored_runners.append({"name": r.get("name"), "raw_score": raw_score})                                              
        # Normalize to percentages
        predictions = []
        for r in sorted(scored_runners, key=lambda x: x["raw_score"], reverse=True):
            win_prob = (r["raw_score"] / total_score) * 100 if total_score > 0 else 0
            predictions.append({
                "runner": r["name"],
                "win_prob": f"{win_prob:.1f}%"
            })
        return predictions
