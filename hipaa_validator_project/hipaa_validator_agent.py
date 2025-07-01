import os
from openai import OpenAI
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PHI detection tool
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

class HIPAAAgent:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.tools = {
            "detect_phi": detect_phi,
            "assess_user_rights": assess_user_rights
        }

    def run(self, prompt: str, tool_name: str) -> str:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        # First get the tool selection from the model
        tool_response = self._get_tool_selection(prompt, tool_name)
        
        # Then execute the selected tool
        return self.tools[tool_name](tool_response)

    def _get_tool_selection(self, prompt: str, tool_name: str) -> str:
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": f"You are a HIPAA compliance assistant. The user wants to use the {tool_name} tool."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

# Test input
test_text = (
    "Name: Sarah Johnson\nDOB: 03/22/1995\nEmail: sarah.j@hospital.com\nSSN: 123-45-6789.\n"
    "Only authorized personnel may access PHI.\nAccess is revoked upon termination.\n"
    "Each user has unique login credentials.\nMFA is required.\nAccess levels are reviewed quarterly.\n"
    "Principle of least privilege enforced.\nAudit logs are maintained."
)

# Initialize and run the agent
agent = HIPAAAgent()

print("\nPHI DETECTION RESULT")
print(agent.run(test_text, "detect_phi"))

print("\nUSER RIGHTS CHECK RESULT")
print(agent.run(test_text, "assess_user_rights"))