import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env



app = FastAPI()

# Optional: Enable CORS if you host frontend separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# S3 client setup
s3_client = boto3.client('s3')
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"message": f"File '{file.filename}' uploaded successfully"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return {"files": files}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_name}")
async def get_download_url(file_name: str):
    try:
        download_url = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': BUCKET_NAME, 'Key': file_name},
                                                        ExpiresIn=3600)
        return {"download_url": download_url}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
