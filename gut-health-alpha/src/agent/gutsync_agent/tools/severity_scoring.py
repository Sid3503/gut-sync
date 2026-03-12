class SeverityScoring:
    def calculate(self, risk_factors: list) -> str:
        print(f"  [Tool] SeverityScoring: Evaluating {len(risk_factors)} risk factors...")
        # Heuristic bump if multiple risk factors
        if len(risk_factors) > 2:
            return "moderate"
        return "mild"
