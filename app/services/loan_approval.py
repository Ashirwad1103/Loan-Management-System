class LoanApproval:
    @staticmethod
    def approve(risk_score):
        if risk_score >= 70:
            return "Approved"
        else:
            return "Rejected"
 
