from fastapi import FastAPI, File, UploadFile
import os
from pdf2docx import Converter # Changed to import Converter class
import uuid
import shutil
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import Any, Dict
from services.cleanfiles import cleanup_file
from services.pdf2wordconverter import convert_pdf_to_docx



app = FastAPI()



@app.get('/')
def home() -> Dict[str, str]:
    """Simple health check endpoint."""
    return {'hello': 'this is the homepage'}


@app.get('/health')
def health():
    return {'status':'ok','version':1}

@app.post('/pdf2word')
async def pdftowordconverter(file: UploadFile):
    """
    Handles file upload, calls the dedicated conversion function, 
    and manages final response/cleanup.
    """
    # 1. Define paths for temporary files
    unique_id = uuid.uuid4()
    pdf_path = f"temp_{unique_id}.pdf"
    docx_path = f"temp_{unique_id}.docx"
    
    # 2. Save the uploaded file
    try:
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        cleanup_file(pdf_path)
        return {"error": f"Failed to save uploaded PDF: {e!r}"}
    
    # 3. Perform conversion (delegated to separate function)
    try:
        convert_pdf_to_docx(pdf_path, docx_path)
    except RuntimeError as e:
        # If conversion fails, ensure both files are cleaned up and return JSON error
        cleanup_file(pdf_path)
        cleanup_file(docx_path)
        return {"error": f"Conversion failed: {e!r}. The resulting DOCX file could not be finalized."}

    # 4. Success: Prepare FileResponse with background cleanup

    # Remove the input PDF file immediately after conversion.
    cleanup_file(pdf_path)

    # Use BackgroundTask to delete the output DOCX file *after* it has been served.
    filename = f"{file.filename.split('.')[0]}.docx"
    
    return FileResponse(
        path=docx_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        background=BackgroundTask(cleanup_file, docx_path)
    )




if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)












# from fastapi import FastAPI,File,UploadFile
# import os
# from pdf2docx import parse
# import uuid
# import shutil
# from fastapi.responses import FileResponse
# from services.cleanfiles import cleanup_file
# from fastapi.background import BackgroundTasks

# app = FastAPI()

# @app.get('/')
# def home():
#     return {'hello':'this is the homepage'} 

# @app.post('/pdf2word')
# async def pdftowordconverter(file:UploadFile):
#     pdf_path = f"temp_{uuid.uuid4()}.pdf"
#     docx_path = f"temp_{uuid.uuid4()}.docx"
    
#     try:
#         with open(pdf_path,"wb") as buffer:
#             shutil.copyfileobj(file.file,buffer)
#     except Exception as e:
#         return {"error": f"Failed to save uploaded PDF: {e!r}"}

#     try:
#         print(f"[INFO] Start to convert {pdf_path}")
#         # Convert PDF to DOCX using parse (simpler than Converter)
#         parse(pdf_path, docx_path)
#         if not os.path.exists(docx_path):
#             raise RuntimeError("Conversion failed: Output DOCX file was not generated.")
#     except Exception as e:
#         cleanup_file(pdf_path)
#         cleanup_file(docx_path)
#         return {"error": f"Conversion failed: {e!r}. Please check the PDF content or library dependencies (pdf2docx/PyMuPDF)."}
        

#     cleanup_file(pdf_path)

#     return FileResponse(path=docx_path,filename=f"{file.filename.split('.')[0]}.docx",media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#                         background=BackgroundTasks(cleanup_file, docx_path))


# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8080)) 
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=port)

    
