class ReportGenerator:

    @staticmethod
    def generate(email, llm_output, risk_output):
        return {
            "emailId": email["emailId"],
            "from": email["from"],
            "to": email["to"],
            "subject": email["subject"],
            "compliance_flag": llm_output["compliance_flag"],
            #"classification": llm_output["classification"],
            "categories": llm_output["categories"],
            "confidence": llm_output["confidence"],
            "reason": llm_output["reason"],
            "evidence": llm_output["evidence"],
            "risk_score": risk_output["risk_score"],
            "priority": risk_output["priority"]
        }
