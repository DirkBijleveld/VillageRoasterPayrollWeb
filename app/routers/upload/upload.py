from fastapi import APIRouter, UploadFile
from starlette.concurrency import run_in_threadpool

from app.csv.csv import read_file, get_payroll_period

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_file(file: UploadFile):
    """
    Allows client to upload a file to server.
    Reads the file and payroll period to allow for session creation.
    """
    # file.file provides the read_file() function with a file-like object
    df = read_file(file.file)
    # File must be re-buffered to be read again
    await file.seek(0)
    # Get payroll period from file
    payroll_period = get_payroll_period(file.file)
    # TEMP: Return a json response
    return {
        "filename": file.filename,
        "payroll_period": payroll_period,
        "size": len(df)
    }
