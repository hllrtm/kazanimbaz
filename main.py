from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# ---- HTML ANA SAYFA ----
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

# ---- PDF YÜKLEME ----
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        file_path = f"pdfs/{file.filename}"

        supabase.storage.from_("pdfs").upload(file_path, file_bytes)

        return JSONResponse({"message": "PDF başarıyla yüklendi!"})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
