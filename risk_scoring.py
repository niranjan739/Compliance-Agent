from  config.settings import CATEGORY_WEIGHTS

class RiskScoring:

    @staticmethod
    def calculate(categories, confidence):
        """Calculate risk score and priority.

        categories: iterable of category keys used in CATEGORY_WEIGHTS
        
        
        """
        category_score = sum(
            CATEGORY_WEIGHTS.get(category, 0) for category in categories
        )

        confidence_score = int(confidence * 0.40)

        risk_score = min(100, category_score + confidence_score)

        if risk_score >= 90:
            priority = "Critical"
        elif risk_score >= 70:
            priority = "High"
        elif risk_score >= 40:
            priority = "Medium"
        else:
            priority = "Low"

        return {
            "risk_score": round(risk_score),
            "priority": priority,
        }