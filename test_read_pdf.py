# test_read_pdf.py
from tools import FinancialDocumentTool

if __name__ == "__main__":
    path = "data/sample.pdf"
    try:
        text = FinancialDocumentTool.read_data_tool(path)
        print("Read OK. Length (chars):", len(text))
        print("First 1000 chars:\n")
        print(text[:1000])
    except Exception as e:
        print("Error reading PDF:", e)
