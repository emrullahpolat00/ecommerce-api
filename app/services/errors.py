from fastapi import HTTPException

def not_found(entity: str):
    raise HTTPException(status_code=404, detail=f"{entity} not found")

def bad_request(msg: str):
    raise HTTPException(status_code=400, detail=msg)