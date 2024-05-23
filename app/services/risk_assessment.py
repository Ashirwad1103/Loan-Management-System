class RiskAssessment:
    @staticmethod
    def assess(loan_application):
        score = 0
        score += (loan_application.credit_score / 850) * 40
        score += (1 - loan_application.debt_to_income_ratio) * 20
        score += 20 if loan_application.employment_status == "Employed" else 0
        score += (loan_application.income / loan_application.loan_amount) * 20
        return score
 
