"""
PaddleOCR integration for extracting text from PDFs and images.
"""
from paddleocr import PaddleOCR
from pathlib import Path
from typing import List, Dict, Optional
import logging
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FIX 1: REMOVED GLOBAL INITIALIZATION ---
# ocr_engine = PaddleOCR(...)  <-- DELETED THIS LINE

class OCRProcessor:
    """Handles OCR processing for documents."""
    
    def __init__(self):
        # --- FIX 2: Initialize as None ---
        self.ocr = None
    
    def _get_ocr_engine(self):
        """Lazy load the OCR engine only when needed."""
        if self.ocr is None:
            logger.info("⏳ Loading OCR Model for the first time... (This may take a few seconds)")
            # --- FIX 3: Force CPU mode ---
            # use_gpu=False is critical for Render Free Tier
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)
            logger.info("✅ OCR Model loaded successfully!")
        return self.ocr

    def process_document(self, file_path: str) -> str:
        from config import settings
        
        if settings.USE_MOCK_OCR:
            from ocr.mock_ocr_data import get_mock_ocr_text
            filename = Path(file_path).name
            logger.info(f"🚀 USING MOCK OCR for {filename}")
            return get_mock_ocr_text(filename)
        
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            return self.extract_text_from_image(file_path)
        else:
            logger.error(f"Unsupported file type: {extension}")
            return ""
    
    def extract_text_from_image(self, image_path: str) -> str:
        try:
            start_time = time.time()
            logger.info(f"Processing image: {image_path}")
            
            # --- FIX 4: Use the lazy getter ---
            engine = self._get_ocr_engine()
            result = engine.ocr(image_path, cls=True)
            
            if not result or result[0] is None:
                logger.warning(f"No text found in {image_path}")
                return ""
            
            text_lines = []
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                if 'rec_texts' in result[0]:
                    text_lines = result[0]['rec_texts']
            elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                for line in result[0]:
                    if len(line) >= 2:
                        text = line[1][0]
                        text_lines.append(text)
            
            full_text = "\n".join(text_lines)
            elapsed = time.time() - start_time
            logger.info(f"[TIMING] Image OCR took {elapsed:.2f}s")
            return full_text
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        # (This function stays mostly the same, just ensure it calls self.extract_text_from_image)
        total_start = time.time()
        try:
            from pdf2image import convert_from_path
            import tempfile
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Limit thread_count to 1 to save memory
                images = convert_from_path(pdf_path, output_folder=tmp_dir, thread_count=1)
                
                all_text = []
                for i, image in enumerate(images):
                    img_path = os.path.join(tmp_dir, f"page_{i}.jpg")
                    image.save(img_path, 'JPEG')
                    
                    page_text = self.extract_text_from_image(img_path)
                    if page_text:
                        all_text.append(f"--- Page {i+1} ---\n{page_text}")
                
                return "\n\n".join(all_text)
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return ""

# Global OCR processor instance
ocr_processor = OCRProcessor()