from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from supabase import create_client
from dotenv import load_dotenv
import os

# -----------------------------
# ENV YÜKLEME
# -----------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY (first 10 chars):", SUPABASE_KEY[:10])

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI()


# ----------------------------------------------------
# 1) ANA SAYFA → index.html dosyasını görüntüleme
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    # index.html aynı klasördeyse direkt döner
    return FileResponse("index.html")


# ----------------------------------------------------
# 2) PDF UPLOAD ENDPOINT
# ----------------------------------------------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        file_path = f"pdfs/{file.filename}"

        # Supabase storage'a yükle
        supabase.storage.from_("pdfs").upload(file_path, file_bytes)

        return JSONResponse({"message": "PDF başarıyla yüklendi!"})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
