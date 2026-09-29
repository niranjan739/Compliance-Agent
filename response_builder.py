class ResponseBuilder:

    @staticmethod
    def build(report):
        return {
            "emailId": report["emailId"],
            "status": "Flagged" if report["compliance_flag"] else "Compliant",
            #"classification": report["classification"],
            "categories": report["categories"],
            "evidence": report["evidence"],
            "reason": report["reason"],
            "risk_score": report["risk_score"],
            "priority": report["priority"],
        }
