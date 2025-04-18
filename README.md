# TDS Project One – Graded Assignment Solver

This project is a **function-call based** application designed to automate the process of solving **54 graded assignment questions** from the *Tools in Data Science* course by **IIT Madras Online Degree**.

The application provides an API endpoint that takes a question and optional file attachments (such as zipped files) as input, and returns the answer in the required format, which can be directly submitted in the assignments.

##  Project Overview

The **TDS Project One** app is built using **FastAPI**, hosted on **Azure**, and is integrated with **GitHub Actions** for continuous deployment. It leverages **function calling** mechanisms to map questions to predefined answers, streamlining the solution process.

##  Technologies Used

| Technology Stack     | Description |
|----------------------|-------------|
| **Backend**          | Python, FastAPI |
| **Function Calling** | Custom function call logic to handle dynamic questions |
| **Deployment**       | Hosted on Azure with CI/CD integration via GitHub Actions |
| **File Handling**    | Supports file uploads (e.g., ZIP files) via API requests |

## 📤 API Usage

### Sample `curl` Request:
```bash
curl -X POST "https://your-app.azurewebsites.net/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip. What is the value in the 'answer' column?" \
  -F "file=@abcd.zip"
```
Expected JSON Response:
{
  "answer": "1234567890"
}

## Features
Dynamic Question Handling: Accepts questions from the five graded assignments and returns the correct answer.

Function Calling: Implements a function-call-based solution to match each question to its specific handler.

File Upload: Supports ZIP file uploads, where files can be processed to extract necessary answers.

CI/CD: Deployed automatically using GitHub Actions to Azure, ensuring continuous integration and delivery.

Real-Time Answer Generation: Returns answers that can be directly input into the assignments.

## Setup and Installation
Clone the repository:

git clone https://github.com/INCURSIA/TDS-Solver.git
Install dependencies:

Ensure Python 3.9+ is installed.

Create a virtual environment:

python3 -m venv venv
Install required packages:


pip install -r requirements.txt
Run the app locally:

uvicorn app.main:app --reload
Access the API:

The API will be accessible at http://127.0.0.1:8000/api/ on your local machine.

