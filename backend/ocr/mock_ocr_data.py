"""
Mock OCR results for testing/development
Supports multiple document types for comprehensive testing
"""

MOCK_OCR_DATA = {
    "bill": """Medical Bill
Patient Name: Emily Davis
Provider: Valley Care Clinic
Date of Service: 2024-08-31
Procedure: CT Abdomen
CPT Code: 74160
Amount Charged: $1775
Billing ID: BL-314225
Patient Insurance: BlueCross PPO
Member ID: BCB123456789""",
    
    "doctor": """VALLEY CARE CLINIC
Medical Consultation Note

Patient Name: Emily Davis
Date: 2024-08-31
Chief Complaint: Severe abdominal pain

Assessment:
Patient presents with acute abdominal pain in lower right quadrant.
Clinical examination suggests possible appendicitis or ovarian cyst.
Pain severity: 8/10, worsening over past 24 hours.

Medical Necessity:
CT Abdomen with contrast (CPT 74160) is medically necessary to:
- Rule out acute appendicitis
- Evaluate for ovarian pathology
- Assess for other acute intra-abdominal processes

Plan:
Order CT abdomen immediately
Patient instructed to proceed to imaging center
Follow-up after imaging results

Physician: Dr. Sarah Johnson, MD
License: CA-12345
Date: 2024-08-31""",
    
    "insurance": """BLUECROSS BLUESHIELD PPO
Insurance Card

Member Name: EMILY DAVIS
Member ID: BCB123456789
Group Number: GRP-5544
Plan: PPO Plus
Effective Date: 01/01/2024

Coverage:
- In-Network: 80% coverage
- Out-of-Network: 60% coverage
- Deductible: $1000 (Individual)

Customer Service: 1-800-123-4567
Pre-Authorization Required for:
CT/MRI, Surgery, Hospitalization""",
    
    "preauth": """BLUECROSS BLUESHIELD
PRE-AUTHORIZATION APPROVAL

Patient: Emily Davis
Member ID: BCB123456789
Date: 2024-08-30
Authorization Number: AUTH-2024-88172

APPROVED PROCEDURE:
CT Abdomen with Contrast
CPT Code: 74160
Provider: Valley Care Clinic
NPI: 1234567890

This procedure has been reviewed and approved by our medical review team based on medical necessity documentation provided.

Status: APPROVED
Authorized Date of Service: 2024-08-31
Valid Through: 2024-09-15

BlueCross BlueShield Medical Review Department"""
}


def get_mock_ocr_text(filename: str) -> str:
    """
    Get mock OCR text based on filename pattern.
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        Appropriate mock OCR text for the document type
    """
    filename_lower = filename.lower()
    
    # Match filename patterns to document types
    if "bill" in filename_lower or "invoice" in filename_lower:
        return MOCK_OCR_DATA["bill"]
    elif "doctor" in filename_lower or "note" in filename_lower or "consultation" in filename_lower:
        return MOCK_OCR_DATA["doctor"]
    elif "insurance" in filename_lower or "card" in filename_lower:
        return MOCK_OCR_DATA["insurance"]
    elif "auth" in filename_lower or "approval" in filename_lower or "preauth" in filename_lower:
        return MOCK_OCR_DATA["preauth"]
    else:
        # Default to bill if pattern doesn't match
        return MOCK_OCR_DATA["bill"]
