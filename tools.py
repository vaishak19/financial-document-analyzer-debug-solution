# # tools.py
# import re

# try:
#     import PyPDF2
#     _HAS_PYPDF2 = True
# except Exception:
#     _HAS_PYPDF2 = False


# def read_data(path: str) -> str:
#     """
#     Read a PDF or text file and return cleaned text (UTF-8).
#     Always returns a string. Raises FileNotFoundError on missing file.
#     """
#     if not isinstance(path, str) or not path.strip():
#         raise ValueError("path must be a non-empty string")

#     text = ""
#     try:
#         if _HAS_PYPDF2 and path.lower().endswith(".pdf"):
#             with open(path, "rb") as f:
#                 reader = PyPDF2.PdfReader(f)
#                 for page in reader.pages:
#                     page_text = page.extract_text() or ""
#                     text += page_text + "\n"
#         else:
#             with open(path, "rb") as f:
#                 raw = f.read()
#             text = raw.decode("utf-8", errors="replace")
#     except FileNotFoundError:
#         raise
#     except Exception as e:
#         raise RuntimeError(f"Could not read file {path}: {e}")

#     text = re.sub(r"\r\n", "\n", text)
#     text = re.sub(r"\n{2,}", "\n", text)
#     text = re.sub(r"[ \t]{2,}", " ", text)
#     return text.strip()


# class SimpleTool:
#     """Lightweight wrapper so functions can be used as CrewAI tools without BaseTool."""

#     def __init__(self, name: str, description: str, func):
#         self.name = name
#         self.description = description
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         return self.func(*args, **kwargs)


# # Create tool instances
# FinancialDocumentTool = SimpleTool(
#     name="read_data",
#     description="Reads a PDF or text file and returns cleaned text for financial analysis.",
#     func=read_data,
# )


# tools.py
import os
from dotenv import load_dotenv
load_dotenv()

# If you prefer a different pdf library adjust imports & requirements accordingly.
# Add 'pypdf' to requirements.txt if not already present.
try:
    from pypdf import PdfReader
except Exception as e:
    raise RuntimeError("Please install pypdf (add to requirements) or adjust tools.py to use another PDF loader.") from e

# Optional: search tool import (ensure you have credentials)
# from crewai_tools.tools.serper_dev_tool import SerperDevTool
# search_tool = SerperDevTool()

class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        """
        Read a PDF from disk and return extracted text.
        Returns an empty string on failure and raises on missing file.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        reader = PdfReader(path)
        full_report = []
        for page in reader.pages:
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            # normalize whitespace
            text = text.replace("\r\n", "\n")
            while "\n\n" in text:
                text = text.replace("\n\n", "\n")
            full_report.append(text)

        return "\n".join(full_report)

class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> str:
        """
        Placeholder: sanitize the extracted text and provide a basic summary.
        Extend this with real analysis logic.
        """
        if not financial_document_data:
            return "No financial data provided."

        # Simple cleaning: collapse repeated spaces
        processed = " ".join(financial_document_data.split())
        # TODO: implement real investment analysis pipeline here
        return "Investment analysis functionality to be implemented (placeholder)."

class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented (placeholder)."
