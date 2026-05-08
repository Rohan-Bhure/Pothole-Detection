from fastapi import APIRouter, Form

router = APIRouter()

# Temporary storage (later replace with DB)
reports_db = {}

@router.post("/verify-report")
async def verify_report(
    report_id: str = Form(...),
    is_valid: bool = Form(...),
    name: str = Form(...),
    phone: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):

    if not is_valid:
        return {
            "status": "rejected",
            "message": "User rejected the detection. No complaint created."
        }

    # Create complaint
    complaint = {
        "report_id": report_id,
        "user": name,
        "phone": phone,
        "location": {
            "lat": latitude,
            "lon": longitude
        },
        "status": "pending",
        "priority": "HIGH" if latitude else "MEDIUM"
    }

    reports_db[report_id] = complaint

    return {
        "status": "complaint_created",
        "complaint": complaint,
        "message": "✅ Complaint successfully registered"
    }