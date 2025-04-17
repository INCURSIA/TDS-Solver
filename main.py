from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Form, APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import os
import json
from ga.ga1 import question1, question2, question3, question4, question5, question6, question7, question8, question9,question10, question13, question11, question12,question14,question15, question16, question17, question18
from ga.ga2 import ga2_question1, ga2_question2, ga2_question3, ga2_question4, ga2_question5, ga2_question6,ga2_question7, ga2_question9
from ga.ga3 import ga3_question1, ga3_question2, ga3_question3, ga3_question4 ,ga3_question5, ga3_question6, ga3_question7, ga3_question8
from ga.ga4 import  ga4_question1, ga4_question2, ga4_question3, ga4_question4, ga4_question5, ga4_question6, ga4_question7, ga4_question8, ga4_question9,ga4_question10
from ga.ga5 import ga5_question1, ga5_question2, ga5_question3, ga5_question4, ga5_question5,ga5_question6,ga5_question7,ga5_question8, ga5_question10,ga5_question9

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Create a router for dynamically adding endpoints
router = APIRouter()
# Ensure the data folder exists
DATA_FOLDER = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

# Get current directory of the project
# BASE_DIR = os.path.join(os.getcwd(), "ffmpeg")
# # Set FFmpeg binary path manually
# # FFMPEG_PATH = os.path.join(BASE_DIR, "bin", "ffmpeg.exe")


# Set up templates directory (extra part added for rendering HTML)
# templates = Jinja2Templates(directory="templates")
# @app.get("/")
# def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
# Set up templates directory (extra part added for rendering HTML)


@app.post("/api/")
async def process_question(
    question: str = Form(...),  # Extract "question" from form data
    file: UploadFile = None    # Handle file uploads
):
    if not question:
        return JSONResponse({"error": "No question provided"}, status_code=400)

    # Initialize temp_path to None
    temp_path = None 
    # Save uploaded file to the data folder
    if file:
        temp_path = os.path.join(DATA_FOLDER, file.filename)
        with open(temp_path, "wb") as f:
            f.write(await file.read())

    # # Handle file upload to Azure Blob Storage
    # if file:
    #     blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    #     blob_client.upload_blob(await file.read(), overwrite=True)
    #     temp_path = os.path.join(DATA_FOLDER, file.filename)  # Temporary file path for processing

    #     # Download the file from Azure Blob Storage to /tmp for processing
    #     with open(temp_path, "wb") as temp_file:
    #         download_stream = blob_client.download_blob()
    #         temp_file.write(download_stream.readall())

# ------------------------ GA1--------------------------------

    if "What is the output of code -s" in question:
        answer = question1.code_s()
    
    elif "Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter" in question:
        answer = question2.output(question)
    
    elif "prettier" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "README.md")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)    
        answer = question3.solve_question(temp_path)

    elif "ARRAY_CONSTRAIN(SEQUENCE" in question:  
        answer = question4.solve_google_sheets(question)

    elif "SUM(TAKE(SORTBY" in question:
        answer = question5.solve_excel_formula(question)
    
    elif "What is the value in the hidden input" in question:
        with open(temp_path, "r", encoding="utf-8") as f:
            answer = question6.output(f)

    elif "are there in the date range" in question:
        answer = question7.count_weekdays_in_range(question)

    elif "column of the CSV" in question:
        # Use default file if no file is uploaded
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-extract-csv-zip.zip")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        
        with open(temp_path, "rb") as f:  # Open file in binary mode
            answer = question8.process_zip(f)  # Pass file object instead of path
    
    elif "Sort this JSON array of objects by the value of the" in question:  
        answer = question9.sort_json(question)

    elif "convert it into a single JSON object, where key=value pairs are converted into" in question:
        answer= question10.main(temp_path)

    elif "having a foo class in the hidden element below" in question:
        with open(temp_path, "r", encoding="utf-8") as f:
            answer = question11.output(f)

    elif "What is the sum of all values associated with these symbols" in question:
        answer = question12.main(temp_path, question)

    elif "Create a new public repository. Commit a single JSON file called email.json with the value" in question:
        answer = question13.create_github_repo_with_email(question)
 
    elif "unzip it into a new folder, then replace all" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-list-files-attributes.zip")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "rb") as f:
            answer = question14.process_zip_file(f,question)

    elif "What's the total size of all files at least" in question:
        # Use default file if no file is uploaded
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-list-files-attributes.zip")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "rb") as f:
            answer = question15.process_zip(f, question)
    
    elif "What does running grep . * | LC_ALL=C sort | sha256sum" in question:
        # Use default file if no file is uploaded
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-move-rename-files.zip")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "rb") as f:
            answer = question16.process_zip_file(f)

    elif "How many lines are different between " in question:
        # Use default file if no file is uploaded
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-compare-files.zip")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "rb") as f:
            answer = question17.function_name(f)
    elif "What is the total sales of all the items in the" in question:
        answer = question18.generate_sql(question)

# ------------------------ GA2--------------------------------
    elif "Write documentation in Markdown" in question:
        answer = ga2_question1.get_markdown()
    
    elif "Download the image below and compress it losslessly" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "shapes.png")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        # Pass the file path to the function
        answer = ga2_question2.compress_image_to_base64(question, temp_path)

    elif "Publish a page using GitHub Pages that showcases your work" in question:
        answer = ga2_question3.publish_github_pages_with_email(question)

    elif "Run this program on Google Colab, allowing all required access" in question:
        answer = ga2_question4.extract_email_hash(question)
    
    elif "calculate the number of pixels" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "works.png")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        answer=ga2_question5.process_image(question, temp_path)

    elif "Create and deploy a Python app to Vercel" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-vercel-python.json")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        answer = ga2_question6.handle_vercel_deploy(temp_path)
    
    elif "Make sure one of the steps in the action has a name that contains your email address" in question:
        answer = ga2_question7.run_question_server_github(question)

    elif "Return students in the same order as they appear in the CSV file" in question:
        student_endpoint = ga2_question9.run_question_server(temp_path)
        router.add_api_route(
            path="/set",
            endpoint=student_endpoint,
            methods=["GET"],
        )
        app.include_router(router)
        
        base_url = "127.0.0.1:8000"
        api_url = f"{base_url}/set"
        answer = api_url




# ------------------------ GA3--------------------------------
    elif "a sample piece of meaningless" in question:
        answer = ga3_question1.generate_sentiment_analysis_code(question)

    elif "many input tokens does it use" in question:
        answer = ga3_question2.estimate_token_usage(question)

    elif "Uses structured outputs to respond with an object addresses which is an array of objects with required fields:" in question:
        answer= ga3_question3.generate_json_body(question)

    elif "for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "works.png")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        answer=ga3_question4.process_image(question, temp_path)

    elif "text embedding for the 2 given personalized transaction verification messages above." in question:
        answer=ga3_question5.generate_text_embedding_payload(question)

    elif "calculate the cosine similarity between each pair of these embeddings and return the pair" in question:
        answer=ga3_question6.detect_and_generate_code(question)

    elif "build a FastAPI POST endpoint that accepts an array of docs and query string via a JSON body" in question:
        # answer=ga3_question7.run_question_server()
       # Dynamically add the similarity endpoint
        similarity_endpoint = ga3_question7.run_question_server7()
        router.add_api_route(
            path="/similarity",
            endpoint=similarity_endpoint,
            methods=["POST"],
        )
        app.include_router(router)

        # Construct the URL for the similarity endpoint
        base_url = "127.0.0.1:8000"  # Replace <your-app-name> with your Azure app name
        similarity_url = f"{base_url}/similarity"
        answer = similarity_url

    elif "Analyzes the q parameter to identify which function should be called" in question:
        # answer=ga3_question8.run_question_server()
        # Dynamically add the execute endpoint
        execute_endpoint = ga3_question8.run_question_server8()
        router.add_api_route(
            path="/execute",
            endpoint=execute_endpoint,
            methods=["GET"],
        )
        app.include_router(router)

        # Construct the URL for the execute endpoint
        base_url = "127.0.0.1:8000"  # Replace <your-app-name> with your Azure app name
        execute_url = f"{base_url}/execute"
        answer = execute_url


# ------------------------ GA4--------------------------------
    elif "total number of ducks across players" in question:
        answer = ga4_question1.get_total_ducks(question)

    elif "Utilize IMDb's advanced web search" in question:
        answer = ga4_question2.fetch_filtered_imdb_titles(question)

    elif "fetch the Wikipedia page of the country"  in question:
        # answer = ga4_question3.get_wikipedia_page(question)
        # Dynamically add the outline endpoint
        outline_endpoint = ga4_question3.run_question_server3()
        router.add_api_route(
            path="/outline",
            endpoint=outline_endpoint,
            methods=["GET"],
        )
        app.include_router(router)

        # Construct the URL for the outline endpoint
        base_url = "https://ga-solver-tool-geh2bee5h7ejgdet.centralindia-01.azurewebsites.net"  # Replace <your-app-name> with your Azure app name
        outline_url = f"{base_url}/outline"
        answer = outline_url

    elif "weather forecast for" in question:
        answer = ga4_question4.get_bbc_weather_by_city(question)

    elif "latitude of the bounding box" in question: #modification of string minimum or maximum
        answer = ga4_question5.get_latitude(question)

    elif "latest Hacker News post mentioning" in question:
        answer = ga4_question6.get_latest_post_link(question)

    elif "newest user joined GitHub" in question:
        answer= ga4_question7.get_github_users(question)
    elif "Create a scheduled GitHub action that runs daily and adds a commit to your repository" in question:
        answer= ga4_question8.create_daily_commit_repo(question)
    
    elif "marks of students who scored" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-extract-tables-from-pdf.pdf")  # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)    
        answer = ga4_question9.main(temp_path, question)
    elif "Convert the PDF file to Markdown" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-pdf-to-markdown.pdf")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        answer = ga4_question10.main(temp_path)   

# ------------------------ GA5--------------------------------

    elif "What is the total margin for transactions before" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-clean-up-excel-sales-data.xlsx")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "rb") as f:
            answer = ga5_question1.calculate_total_margin(f, question)
    
    elif "How many unique students are there in the file" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-clean-up-student-marks.txt")
        with open(temp_path, "r", encoding="utf-8") as f:
            answer = ga5_question2.count_unique_students(f)
    
    elif "successful GET requests for pages under" in question:
        log_file_path = os.path.join(DATA_FOLDER, "s-anand.net-May-2024.gz")
        answer = ga5_question3.process_question_and_count_requests(question, log_file_path)
    
    elif "how many bytes did the top IP address" in question:
        log_file_path = os.path.join(DATA_FOLDER, "s-anand.net-May-2024.gz")  
        answer = ga5_question4.main(question,log_file_path)

    elif "How many units of" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-clean-up-sales-data.json")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "r") as f:
            answer = ga5_question5.count_food_sales(f,question)

    elif "What is the total sales value" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-parse-partial-json.jsonl")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "r") as f:
            answer = ga5_question6.total_sales(f)
    
    elif "appear as a key" in question:
        if not temp_path:
            temp_path = os.path.join(DATA_FOLDER, "q-extract-nested-json-keys.json")
        # Default file path
        if not os.path.exists(temp_path):
            return JSONResponse({"error": f"File not found: {temp_path}"}, status_code=400)
        with open(temp_path, "r") as f:
            answer = ga5_question7.process_data(f,question)

    elif "Write a DuckDB SQL query to find all posts IDs after" in question:
        answer = ga5_question8.generate_duckdb_query(question)
    
    elif "text of the transcript" in question:
        # Define the file path for transcript.csv
        transcript_file_path = os.path.join(DATA_FOLDER, "transcript.csv")    
        # Call the function with both the question and file path
        answer = ga5_question9.process_question_and_get_transcript_with_overlap(question, transcript_file_path)

    elif "reconstructed image by moving the pieces" in question:
        log_file_path = os.path.join(DATA_FOLDER, "reconstructed_image.png")
        answer = ga5_question10.image_to_base64(log_file_path)

    else:
        return JSONResponse({"error": "Unsupported question"}, status_code=400)

    return json.dumps({"answer": answer})

# Optional for local test (not required in Azure)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



