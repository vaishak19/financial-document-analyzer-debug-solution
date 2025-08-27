# # app.py
# import os
# import uuid
# import json
# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.responses import JSONResponse

# from crewai import Crew, Process
# from agents import financial_analyst, verifier, investment_advisor
# from tasks import extract_task, verify_task, analysis_task

# app = FastAPI(title="Financial Document Analyzer (debug friendly)")


# def safe_parse(output):
#     """Try to parse JSON string into dict, else return the raw string."""
#     if output is None:
#         return None
#     try:
#         return json.loads(str(output))
#     except Exception:
#         return str(output)


# def run_crew(query: str, file_path: str):
#     """
#     Build a Crew with three sequential tasks and return parsed outputs step by step.
#     """
#     crew = Crew(
#         agents=[financial_analyst, verifier, investment_advisor],
#         tasks=[extract_task, verify_task, analysis_task],
#         process=Process.sequential,
#     )

#     inputs = {"query": query, "file_path": file_path}
#     result = crew.kickoff(inputs)

#     outputs = {
#         "extract_task": safe_parse(extract_task.output.raw if extract_task.output else None),
#         "verify_task": safe_parse(verify_task.output.raw if verify_task.output else None),
#         "analysis_task": safe_parse(analysis_task.output.raw if analysis_task.output else None),
#         "crew_result": str(result),  # full raw Crew result (stringified)
#     }
#     return outputs


# @app.get("/")
# async def root():
#     return {"message": "Financial Document Analyzer running"}


# @app.post("/analyze")
# async def analyze_endpoint(
#     file: UploadFile = File(...),
#     query: str = Form("Extract key financial facts and ratios"),
# ):
#     file_id = str(uuid.uuid4())
#     os.makedirs("data", exist_ok=True)
#     ext = os.path.splitext(file.filename)[1] or ".pdf"
#     file_path = os.path.join("data", f"uploaded_{file_id}{ext}")

#     try:
#         content = await file.read()
#         if not content:
#             raise HTTPException(status_code=400, detail="Uploaded file is empty")
#         with open(file_path, "wb") as f:
#             f.write(content)

#         try:
#             outputs = run_crew(query=query.strip(), file_path=file_path)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Crew execution error: {str(e)}")

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "status": "success",
#                 "query": query,
#                 "file_processed": file.filename,
#                 "outputs": outputs,
#             },
#         )

#     finally:
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#         except Exception:
#             pass


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, verifier, risk_assessor
from tasks import analyze_financial_document as analyze_task

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """Run the crew with the provided query and file path"""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor],
        tasks=[analyze_task],
        process=Process.sequential,
    )

    # Include both query and file path in the kickoff payload
    payload = {"query": query, "file_path": file_path}
    result = financial_crew.kickoff(payload)
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide a comprehensive informational analysis (not financial advice)"""

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"

        # Kick off the Crew with both query and file_path
        response = run_crew(query=query.strip(), file_path=file_path)

        # The Crew result may already be JSON-serializable; stringify safely
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
