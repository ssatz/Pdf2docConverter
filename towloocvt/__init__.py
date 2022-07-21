import fitz
from io import BytesIO
from pdf2docx import Converter
from pdf2docx.page.Pages import Pages
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomConverter(Converter):
    def __init__(self, pdf_file:str, password:str=None):
        self.filename_pdf = pdf_file
        self.password = str(password or '')
        self._fitz_doc = fitz.Document(stream=pdf_file)
        self._pages = Pages()


@app.post("/convert", response_class=FileResponse)
async def convert_pdf_to_docx(
    file: UploadFile = File(..., description="A file read as UploadFile")
):
    obj = BytesIO(file.file.read())
    cv = CustomConverter(obj)
    cv.convert("docx.docx")
    cv.close()
    obj.close()
    return FileResponse("docx.docx")