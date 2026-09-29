import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

"""endpoint = "https://dev-openai-service-01.openai.azure.com/"
model_name = "gpt-4o"
deployment = "<deployment name in the endpoint URL like teamX-uniqueid>"

subscription_key = "<your-api-key>"
api_version = "2024-12-01-preview"
"""
client = AzureOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("AZURE_OPENAI_Endpoint"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

class ComplianceAgent:
    def analyze_email(self, email):
        prompt = f"""
You are a banking compliance surveillance analyst. Review the email below for a
potential compliance concern. Your role is to identify concerns for review, not
to make a legal finding.

Classify only these exact category names (spelling and capitalization matter):
 1. "Secrecy": concealment, deletion of records, or avoiding required disclosure.
  Do not flag ordinary, legitimate confidentiality language (for example, a
  signed NDA or confidentiality agreement) without an additional concealment concern.

  Intent:
  Identify attempts to conceal, suppress, restrict, or prevent visibility of information, activities, decisions, records, or communications.

  Examples of Intent:
  - Keep information confidential from certain individuals or groups
  - Avoid creating an audit trail
  - Hide transactions, decisions, or activities
  - Restrict disclosure of material information
  - Delete, alter, or withhold records
  - Prevent compliance, legal, or management review

2. "Market Manipulation": coordinated trading or order timing intended to move a
  market or influence price/perception, front-running, collusion, or sharing
  material non-public information.

  Intent:
  Identify communications that suggest influencing market behavior, trading activity, security prices, investor decisions, or the misuse of material non-public information for advantage.

  Examples of Intent:
  - Artificially impact market prices
  - Coordinate trading activity
  - Share insider or confidential market information
  - Influence investor perception through misleading information
  - Front running, collusion, or coordinated trading strategies
  - Exploiting non-public information for financial gain

3. "Market Bribery": a gift, favor, payment, or incentive tied to favorable
  treatment or a business decision.

  Intent:
  Identify attempts to improperly influence business, regulatory, commercial, trading, procurement, or investment decisions through benefits, gifts, favors, payments, or incentives.

  Examples of Intent:
  - Offer rewards in exchange for favorable treatment
  - Influence approval or decision-making
  - Provide undisclosed gifts or entertainment
  - Exchange favors for business opportunities
  - Secure contracts, deals, or approvals through incentives
  - Circumvent fair decision-making processes

4. "Change in Communication": moving business discussions to personal,
  unofficial, unmonitored, or otherwise non-approved communication channels.
  Intent:
  Identify efforts to move communications away from monitored, approved, or auditable business channels.

  Examples of Intent:
  - Move conversation to personal email
  - Use private messaging applications
  - Conduct discussions outside official systems
  - Avoid compliance monitoring or record retention
  - Continue sensitive discussions on unofficial channels
  - Reduce traceability or oversight of communications

5. "Complaints": a customer, service, regulatory, or formal workplace complaint
  that needs review or escalation.

  Intent:
  Identify dissatisfaction, grievances, allegations, escalations, disputes, or concerns raised by customers, employees, regulators, vendors, or other stakeholders.

  Examples of Intent:
  - Report poor service or misconduct
  - Escalate unresolved issues
  - Raise regulatory concerns
  - Express dissatisfaction with products or services
  - Report policy violations or operational failures
  - Request remediation or investigation

6. "Employee Ethics": an alleged or proposed policy/control violation, fraud,
  misrepresentation, incomplete required documentation, or conflict of interest.

   Intent:
   Identify conduct that may violate ethical standards, company policies, regulatory requirements, professional obligations, or fiduciary duties.

   Examples of Intent:
   - Bypass established controls or procedures
   - Misrepresent facts or information
   - Create incomplete or misleading documentation
   - Commit fraud or deceptive practices
   - Engage in conflicts of interest
   - Abuse authority or company resources
   - Violate internal policies, regulations, or standards
   - Conceal errors, misconduct, or compliance breaches

Decision rules:
1. Analyze the email subject and body together to determine compliance concerns. Use the subject only to provide context and improve understanding of the body content.
2. Base the classification only on information explicitly stated in the email or strongly and directly implied by the combined subject and body.
3. Do not flag an email solely because it contains words such as "confidential", "secret", "gift", "personal", or similar terms. Consider the full context and intent of the communication.
4. Set "compliance_flag" to true only when at least one defined compliance category is directly supported by the email content. Otherwise, set it to false.
5. If "compliance_flag" is false:
  - Return an empty array for "categories".
  - Return an empty array for "evidence".
  - Return an empty array for "reason".
  - Set "confidence" to 0.
6. If "compliance_flag" is true:
  - Include each applicable category only once.
  - Include only categories that are directly supported by the email content.
  - Evidence must contain one or more exact, verbatim excerpts taken only from the email body.
  - Do not include any text from the email subject in the evidence field.
  - Do not paraphrase, summarize, modify, or invent evidence.
  - Do not use sender, recipient, CC, BCC, metadata, or email headers as evidence.
7. Each item in "reason" must clearly explain why the corresponding category warrants compliance review and must be directly supported by the body evidence provided.
8. Confidence must be an integer between 0 and 100 representing confidence in the classification based on the available evidence. It should reflect certainty of classification, not severity of the conduct.
9. When the subject suggests a concern but the email body contains no supporting evidence, do not flag the email.
10. The evidence field must contain exact excerpts from the email body only, even if the subject contributed to the overall classification context.
11. Return only valid JSON and no additional text.

Return only valid JSON object matching this schema exactly:
{{
  "compliance_flag": true,
  "categories": [],
  "confidence": range(0-100),
  "evidence": ["exact excerpt from the subject or body"],
  "reason": ["Brief evidence-grounded explanation."]
}}

Email details:
From: {email['from']}
To: {email['to']}
Subject: {email['subject']}
Body: {email['body']}
"""
        

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
              {
                "role": "system",
                "content": "You are a Banking compliance officer."
              },
              {
                "role": "user",
                "content": prompt
              }
            ]
        )
        content= response.choices[0].message.content
        

        if not content or not content.strip():
            choice = response.choices[0]
            raise RuntimeError(
                "The Azure OpenAI response contained no message content. "
                f"finish_reason={choice.finish_reason!r}; "
                f"refusal={getattr(choice.message, 'refusal', None)!r}."
            )

        # This also accepts models that wrap otherwise-valid JSON in a Markdown fence.
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else ""
            if content.rstrip().endswith("```"):
                content = content.rstrip()[:-3].rstrip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Azure OpenAI did not return valid JSON. "
                f"Response: {content[:500]!r}"
            ) from error
