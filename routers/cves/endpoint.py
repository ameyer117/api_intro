from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from crud import cve as crud
from crud.user import get_current_user

from schemas.cve import CVEInDB, CVECreation, CVEUpdate
from schemas.user import User

router = APIRouter(
    prefix="/cves",
    tags=["cves"],
)


@router.get("/", response_model=List[CVEInDB], summary="Retrieve a list of CVEs")
def read_cves(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user)):
    """
    Retrieve a list of CVEs with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    cves = crud.get_cves(skip=skip, limit=limit)
    return cves


@router.get("/{cve_id}", response_model=CVEInDB, summary="Retrieve a specific CVE by ID")
def read_cve(cve_id: str, current_user: User = Depends(get_current_user)):
    """
    Retrieve a CVE by its unique identifier.

    - **cve_id**: The unique CVE identifier (e.g., CVE-2023-12345)
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    cve = crud.get_cve_by_cve_id(cve_id)
    if not cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found")
    return cve


@router.post("/", response_model=CVEInDB, status_code=status.HTTP_201_CREATED, summary="Create a new CVE")
def create_cve_endpoint(cve: CVECreation, current_user: User = Depends(get_current_user)):
    """
    Create a new CVE entry.

    - **cve**: CVE creation payload
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    existing_cve = crud.get_cve_by_cve_id(cve.cve_id)
    if existing_cve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CVE with this ID already exists")

    db_cve = crud.create_cve(cve)
    return db_cve


@router.put("/{cve_id}", response_model=CVEInDB, summary="Update an existing CVE")
def update_cve_endpoint(cve_id: str, cve_update: CVEUpdate, current_user: User = Depends(get_current_user)):
    """
    Update an existing CVE by its ID.

    - **cve_id**: The unique CVE identifier to update
    - **cve_update**: CVE update payload with fields to modify
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    updated_cve = crud.update_cve(cve_id, cve_update)
    if not updated_cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found or no changes made")
    return updated_cve


@router.delete("/{cve_id}", response_model=CVEInDB, summary="Delete a CVE by ID")
def delete_cve_endpoint(cve_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a CVE by its unique identifier.

    - **cve_id**: The unique CVE identifier to delete
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    deleted_cve = crud.delete_cve(cve_id)
    if not deleted_cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found")
    return deleted_cve