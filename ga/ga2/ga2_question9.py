from fastapi import APIRouter, Query, HTTPException
import pandas as pd
from typing import List

# Load CSV data
def load_data(file_path: str):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CSV: {str(e)}")

def run_question_server(file_path: str):
    """
    Handles the API logic directly when called from main.py.
    """
    data_df = load_data(file_path)
    
    async def student_endpoint(class_: List[str] = Query(None, alias="class")):
        try:
            df = data_df.copy()
            if class_:
                df = df[df["class"].isin(class_)]
            students = df.to_dict(orient="records")
            return {"students": students}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
    return student_endpoint
