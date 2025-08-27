# # tasks.py
# from crewai import Task
# from agents import financial_analyst, verifier, investment_advisor
# from tools import FinancialDocumentTool, read_data

# extract_task = Task(
#     description="Read the financial document and extract structured facts as JSON.",
#     expected_output="JSON string with vendor, invoice number, date, currency, items, totals, and evidence.",
#     agent=financial_analyst,
#     tools=[FinancialDocumentTool],
# )

# verify_task = Task(
#     description="Verify numeric consistency, currency codes, and date formats. Correct minor rounding issues.",
#     expected_output="JSON string with validation results, errors, and corrected invoice if needed.",
#     agent=verifier,
#     tools=[FinancialDocumentTool],
# )

# analysis_task = Task(
#     description="Provide a neutral, non-promotional analysis of the validated invoice JSON.",
#     expected_output="Plain-text analysis listing ratios, assumptions, and suggested next steps.",
#     agent=investment_advisor,
#     tools=[FinancialDocumentTool],
# )


# task.py
from crewai import Task

from agents import financial_analyst, verifier, risk_assessor
from tools import FinancialDocumentTool

# Primary analysis task: summarize key metrics and observations
analyze_financial_document = Task(
    description=(
        "Given the uploaded financial document (path provided in input as 'file_path') and the user query, "
        "extract high-level observations: revenue, net income (or loss), key ratio highlights (gross margin, operating margin, debt/equity if available), "
        "and any notable trends. Mark clearly that this is informational only."
    ),
    expected_output=(
        "A concise, evidence-based summary: bullet points for key figures, short paragraph about trends, "
        "and a final 'notes & limitations' section describing where the agent had low confidence."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

# Verification task: confirm file type and extract basic metadata
verification = Task(
    description="Verify that 'file_path' points to a readable PDF, return basic metadata including number of pages and whether tables/figures exist.",
    expected_output="JSON-like dict with keys: is_pdf, page_count, contains_tables, notes",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)

# Risk summary task: neutral risk observations only
risk_assessment = Task(
    description=(
        "Produce a neutral risk summary based on the document: highlight leverage, liquidity indicators, "
        "one-off items, regulatory or market factors mentioned in the report. Provide assumptions and confidence level."
    ),
    expected_output="Bullet list of risk items with short explanations and a confidence score for each.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)
