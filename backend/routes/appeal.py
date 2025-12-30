"""
Appeal letter generation endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uuid
import json
import logging
from pathlib import Path

from database import get_db, UploadedDocument, ExtractedData, GeneratedAppeal
from llm.extract_llm8b import extractor_llm
from llm.reasoning_llm70b import reasoning_llm
from utils.pdf_tools import AppealLetterPDF
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class AppealRequest(BaseModel):
    """Request model for appeal letter generation."""
    document_ids: List[int]
    insurance_plan: str = None


@router.post("/appeal-letter")
async def generate_appeal_letter(
    request: AppealRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an appeal letter PDF.
    
    Requires:
    - Denial letter
    - Doctor note
    - Medical bill
    
    Args:
        request: Appeal request with document IDs
        db: Database session
        
    Returns:
        File download response with PDF
    """
    try:
        session_id = str(uuid.uuid4())
        
        # Retrieve documents
        documents = db.query(UploadedDocument).filter(
            UploadedDocument.id.in_(request.document_ids)
        ).all()
        
        if len(documents) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 documents required (denial letter + supporting docs)"
            )
        
        # Classify and extract from all documents
        extracted_documents = []
        
        for doc in documents:
            if not doc.ocr_text:
                continue
            
            doc_type = extractor_llm.classify_document(doc.ocr_text)
            extracted_fields = extractor_llm.extract_fields(doc.ocr_text, doc_type)
            
            extracted_documents.append({
                "type": doc_type,
                "fields": extracted_fields
            })
        
        # Find required documents
        denial_doc = next((d for d in extracted_documents if d["type"] == "denial_letter"), None)
        doctor_note = next((d for d in extracted_documents if d["type"] == "doctor_note"), None)
        bill_doc = next((d for d in extracted_documents if d["type"] == "medical_bill"), None)
        
        if not denial_doc:
            raise HTTPException(status_code=400, detail="Denial letter is required")
        
        # Load insurance rules if specified
        insurance_rules = None
        if request.insurance_plan:
            rules_file = settings.INSURANCE_RULES_DIR / f"{request.insurance_plan.lower().replace(' ', '_')}.json"
            if rules_file.exists():
                with open(rules_file, 'r') as f:
                    insurance_rules = json.load(f)
        
        # Generate appeal letter text using LLM-70B
        appeal_text = reasoning_llm.generate_appeal_letter(
            denial_data=denial_doc["fields"],
            doctor_note=doctor_note["fields"] if doctor_note else {},
            bill_data=bill_doc["fields"] if bill_doc else {},
            insurance_rules=insurance_rules
        )
        
        # Create PDF
        pdf_filename = f"appeal_letter_{session_id}.pdf"
        pdf_path = settings.UPLOAD_FOLDER / pdf_filename
        
        patient_name = denial_doc["fields"].get("patient_name", "Patient")
        pdf_generator = AppealLetterPDF(str(pdf_path))
        pdf_generator.generate_appeal_letter(appeal_text, patient_name)
        
        # Store in database
        generated_appeal = GeneratedAppeal(
            session_id=session_id,
            appeal_text=appeal_text,
            pdf_path=str(pdf_path),
            denial_risk_score=0  # Can be calculated if needed
        )
        db.add(generated_appeal)
        db.commit()
        
        logger.info(f"Appeal letter generated: {pdf_path}")
        
        # Return PDF file
        return FileResponse(
            path=str(pdf_path),
            filename=f"Appeal_Letter_{patient_name.replace(' ', '_')}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating appeal letter: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
