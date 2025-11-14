from fastapi import FastAPI, UploadFile, File
from supabase import create_client
import uuid
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug için kontrol:
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY (first 10 chars):", SUPABASE_KEY[:10] if SUPABASE_KEY else None)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"message": "Backend çalışıyor!"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = None):
    file_ext = file.filename.split(".")[-1]
    new_name = f"{uuid.uuid4()}.{file_ext}"
    content = await file.read()

    supabase.storage.from_("pdf-uploads").upload(new_name, content)
    url = f"{SUPABASE_URL}/storage/v1/object/public/pdf-uploads/{new_name}"

    supabase.table("pdf_uploads").insert({
        "user_id": user_id,
        "file_name": file.filename,
        "file_url": url
    }).execute()

    return {"status": "success", "url": url}
