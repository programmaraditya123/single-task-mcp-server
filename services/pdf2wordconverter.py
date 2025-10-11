from pdf2docx import Converter
import os

def convert_pdf_to_docx(pdf_path: str, docx_path: str) -> None:
    """
    Core conversion logic using pdf2docx.Converter class.

    Raises RuntimeError if conversion fails or the output file is empty.
    """
    converter = None
    try:
        # Initialize Converter
        converter = Converter(pdf_path)
        
        # Start conversion
        converter.convert(docx_path)
        
        # Explicitly close and finalize the DOCX file
        converter.close()

        # Check if the DOCX file was successfully created and is not empty
        if not os.path.exists(docx_path) or os.path.getsize(docx_path) == 0:
            raise RuntimeError("Output DOCX file was not generated or is empty.")
            
    except Exception as e:
        # Ensure the converter is closed if an exception occurs during conversion
        if converter:
            try:
                converter.close()
            except:
                pass 
        # Re-raise the exception to be caught by the calling function
        raise RuntimeError(f"Conversion process failed: {e!r}") from e