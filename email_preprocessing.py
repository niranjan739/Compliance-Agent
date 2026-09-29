"""import pandas as pd
df = pd.read_json("c:/Users/MrNiranjanKumar/Desktop/Compliance-Agent/emails.json", orient="records")
print(df)
"""

class EmailPreprocessor:

    @staticmethod
    def preprocess(email):

        return {
            "emailId": email.get("emailId"),
            "from": email.get("from", email.get("From", "")).strip(),
            "to": email.get("to", email.get("To", "")).strip(),
            "subject": email.get("subject", email.get("Subject", "")).strip(),
            "body": email.get("body", email.get("Body", "")).strip()
        }
    
    
    
        
    
