import json
import logging
from pathlib import Path

from compliance_agent import ComplianceAgent
from email_preprocessing import EmailPreprocessor
from risk_scoring import RiskScoring
from report_generator import ReportGenerator
from response_builder import ResponseBuilder

INPUT_FILE = "emails.json"
OUTPUT_FILE = "compliance_report.json"
LOG_DIRECTORY = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIRECTORY / "compliance_agent.log"


def configure_logging():
    """Configure file and console logging for each processing run."""
    LOG_DIRECTORY.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


logger = logging.getLogger(__name__)

def main():
    configure_logging()
    logger.info("Starting compliance report generation")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        emails = json.load(file)
    logger.info("Loaded %d email(s) from %s", len(emails), INPUT_FILE)

    agent = ComplianceAgent()
    results = []

    for email in emails:
        email_id = email.get("emailId")
        try:
            cleaned_email = EmailPreprocessor.preprocess(email)
            llm_output = agent.analyze_email(cleaned_email)
            risk_output = RiskScoring.calculate(
                categories=llm_output["categories"],
                confidence=llm_output["confidence"],
            )
            report = ReportGenerator.generate(cleaned_email, llm_output, risk_output)
            results.append(ResponseBuilder.build(report))
            logger.info(
                "Processed emailId=%s status=%s categories=%s",
                email_id,
                "Flagged" if llm_output["compliance_flag"] else "Compliant",
                llm_output["categories"],
            )
        except Exception:
            logger.exception("Failed to process emailId=%s", email_id)
            raise

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    logger.info("Generated %d compliance report(s) in %s", len(results), OUTPUT_FILE)
    print(f"Generated {len(results)} compliance reports")

if __name__ == "__main__":
    main()
     
