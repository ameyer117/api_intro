from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from crud import cve as crud

from schemas.cve import CVEInDB, CVECreation, CVEUpdate

router = APIRouter(
    prefix="/cves",
    tags=["cves"],
)


@router.get("/cves", response_model=List[CVEInDB], summary="Retrieve a list of CVEs")
def read_cves(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of CVEs with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    cves = crud.get_cves(skip=skip, limit=limit)
    return cves


@router.get("/cves/{cve_id}", response_model=CVEInDB, summary="Retrieve a specific CVE by ID")
def read_cve(cve_id: str):
    """
    Retrieve a CVE by its unique identifier.

    - **cve_id**: The unique CVE identifier (e.g., CVE-2023-12345)
    """
    cve = crud.get_cve_by_cve_id(cve_id)
    if not cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found")
    return cve


@router.post("/cves", response_model=CVEInDB, status_code=status.HTTP_201_CREATED, summary="Create a new CVE")
def create_cve_endpoint(cve: CVECreation):
    """
    Create a new CVE entry.

    - **cve**: CVE creation payload
    """
    existing_cve = crud.get_cve_by_cve_id(cve.cve_id)
    if existing_cve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CVE with this ID already exists")

    db_cve = crud.create_cve(cve)
    return db_cve


@router.put("/cves/{cve_id}", response_model=CVEInDB, summary="Update an existing CVE")
def update_cve_endpoint(cve_id: str, cve_update: CVEUpdate):
    """
    Update an existing CVE by its ID.

    - **cve_id**: The unique CVE identifier to update
    - **cve_update**: CVE update payload with fields to modify
    """
    updated_cve = crud.update_cve(cve_id, cve_update)
    if not updated_cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found or no changes made")
    return updated_cve


@router.delete("/cves/{cve_id}", response_model=CVEInDB, summary="Delete a CVE by ID")
def delete_cve_endpoint(cve_id: str):
    """
    Delete a CVE by its unique identifier.

    - **cve_id**: The unique CVE identifier to delete
    """
    deleted_cve = crud.delete_cve(cve_id)
    if not deleted_cve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CVE not found")
    return deleted_cve