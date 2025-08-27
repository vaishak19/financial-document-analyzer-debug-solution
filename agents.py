# agents.py
# import os
# from crewai import Agent
# from tools import FinancialDocumentTool, read_data

# DEFAULT_LLM = os.getenv("DEFAULT_LLM", "default-llm-placeholder")

# financial_analyst = Agent(
#     role="Financial Analyst",
#     goal="Extract financial facts with evidence.",
#     backstory="Evidence-first, conservative extraction.",
#     tools=[FinancialDocumentTool],  # plain function
#     llm=DEFAULT_LLM,
#     max_iter=3,
#     allow_delegation=False,
# )

# verifier = Agent(
#     role="Document Verifier",
#     goal="Check totals, dates, and consistency.",
#     backstory="Conservative validator.",
#     tools=[FinancialDocumentTool],  # plain function
#     llm=DEFAULT_LLM,
#     max_iter=2,
#     allow_delegation=False,
# )

# investment_advisor = Agent(
#     role="Investment Advisor (informational only)",
#     goal="Provide neutral considerations (not advice).",
#     backstory="Supports due diligence by listing assumptions and next steps.",
#     tools=[FinancialDocumentTool],  # no custom tool needed
#     llm=DEFAULT_LLM,
#     max_iter=1,
#     allow_delegation=False,
# )

# agents.py
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent

# Import your tool(s)
from tools import FinancialDocumentTool

# NOTE: You must provide a real llm instance from your environment or from crewai SDK.
# This is a placeholder pattern. Replace with your project's LLM initialization.
# Example:
# from crewai import LLM
# llm = LLM.from_api_key(os.environ["LLM_API_KEY"])
llm = os.environ.get("LLM_OBJECT_PLACEHOLDER")  # Replace this with actual LLM object

if llm is None:
    # Fail early to avoid creating agents with an undefined llm
    raise RuntimeError("LLM not initialized. Set up an llm object and assign it to `llm` in agents.py")

# Experienced financial analyst — informational only
financial_analyst = Agent(
    role="Senior Financial Analyst (Informational Only)",
    goal=(
        "Read the provided financial document and provide an objective, evidence-based analysis. "
        "State clearly that the output is informational only and not financial advice. "
        "If the user asks for investment decisions, recommend consulting a licensed financial professional."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "An experienced analyst who summarizes financial statements, highlights key ratios and "
        "provides observations about trends and risks in plain language."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)

# Document verifier — basic validation of file type & minimal checks
verifier = Agent(
    role="Document Verifier",
    goal=(
        "Check uploaded files to confirm they appear to be financial documents (PDFs) and extract "
        "basic metadata (page count, presence of numbers/tables). If uncertain, indicate clearly."
    ),
    verbose=True,
    memory=False,
    backstory=("A compliance-minded assistant that verifies file format and basic plausibility."),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)

# Risk assessor — produce a conservative risk-summary, not prescriptive recommendations
risk_assessor = Agent(
    role="Risk Assessment Analyst (Informational Only)",
    goal=(
        "Provide a neutral description of potential risk factors visible in the document, "
        "explain assumptions, and avoid prescriptive investment instructions."
    ),
    verbose=True,
    memory=False,
    backstory=("Experienced in risk frameworks and qualitative risk summaries."),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)
