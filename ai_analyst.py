class AIAnalyst:
    def __init__(self):
        self.name = "The Card AI Analyst"
                                                                    
    def analyze_race(self, runners_data):
        """                                                             Analyzes race runners and returns structured insights.
        """                                                             insights = []                                                   for runner in runners_data:                                         score = runner.get("score", 0)
            if score > 80:                                                      verdict = "Strong contender / High Value"
            elif score > 50:                                                    verdict = "Moderate chance / Place candidate"
            else:                                                               verdict = "Outsider"
                                                                            insights.append({
                "runner": runner.get("name"),                                   "verdict": verdict,                                             "score": score
            })                                                          return insights                                         
