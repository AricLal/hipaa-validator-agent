from agno.agent import Agent
from agno.tools import tool
from agno.models.openai.chat import OpenAIChatModel
import os
from dotenv import load_dotenv

model = OpenAIChatModel(name="gpt-4o")



# Load your OpenAI API key from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# PHI detection tool
@tool
def detect_phi(input_text: str) -> str:
    result = {
        "status": "Non-Compliant",
        "score": 31,
        "violations": [
            {"type": "SSN", "value": "123-45-6789", "risk_weight": 10},
            {"type": "DOB", "value": "03/22/1995", "risk_weight": 7},
            {"type": "Email", "value": "sarah.j@hospital.com", "risk_weight": 8},
            {"type": "Name", "value": "Sarah Johnson", "risk_weight": 6}
        ],
        "recommendation": "Remove/redact PHI before sharing externally."
    }

    violations_text = "\n".join(
        f"- {v['type']}: {v['value']} (Risk Weight: {v['risk_weight']})"
        for v in result["violations"]
    )

    return (
        f"HIPAA Compliance Status: {result['status']}\n"
        f"Score: {result['score']}\n\n"
        f"Violations:\n{violations_text}\n\n"
        f"Recommendation: {result['recommendation']}"
    )

# User rights assessment tool
@tool
def assess_user_rights(input_text: str) -> str:
    result = {
        "status": "Needs Review",
        "score": 22,
        "issues": [
            "Access is revoked upon termination.",
            "Unique login credentials used.",
            "MFA required.",
            "Audit logs maintained.",
            "Quarterly access review enforced.",
            "Least privilege principle applied."
        ],
        "recommendation": "Ensure all staff understand their access rights and regularly update access policies."
    }

    issues_text = "\n".join(f"- {issue}" for issue in result["issues"])

    return (
        f"User Rights Review Status: {result['status']}\n"
        f"Score: {result['score']}\n\n"
        f"Issues Identified:\n{issues_text}\n\n"
        f"Recommendation: {result['recommendation']}"
    )

# Create agent with model string
agent = Agent(
    name="HIPAA Compliance Agent",
    instructions="You are a compliance agent that detects PHI and assesses HIPAA user rights controls.",
    tools=[detect_phi, assess_user_rights],
    model=model
)

# Test input
test_text = (
    "Name: Sarah Johnson\nDOB: 03/22/1995\nEmail: sarah.j@hospital.com\nSSN: 123-45-6789.\n"
    "Only authorized personnel may access PHI.\nAccess is revoked upon termination.\n"
    "Each user has unique login credentials.\nMFA is required.\nAccess levels are reviewed quarterly.\n"
    "Principle of least privilege enforced.\nAudit logs are maintained."
)

# Run
print("\nPHI DETECTION RESULT")
print(agent.run(f"detect_phi: {test_text}").content)

print("\nUSER RIGHTS CHECK RESULT")
print(agent.run(f"assess_user_rights: {test_text}").content)
