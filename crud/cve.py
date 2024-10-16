import sys

from pymongo import ReturnDocument
from schemas.cve import CVECreation
from schemas.cve import CVEUpdate
from db import cves_collection
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_cve_by_cve_id(cve_id: str):
    logger.info(f"Getting CVE {cve_id}")
    return cves_collection.find_one({"cve_id": cve_id})

def get_cves(skip: int = 0, limit: int = 100):
    logger.info(f"Getting CVEs with skip={skip} and limit={limit}")
    cursor = cves_collection.find().skip(skip).limit(limit)
    return list(cursor)

def create_cve(cve: CVECreation):
    logger.info(f"Creating CVE {cve.cve_id}")
    db_cve = cve.model_dump()
    result = cves_collection.insert_one(db_cve)
    return cves_collection.find_one({"_id": result.inserted_id})

def update_cve(cve_id: str, cve_update: CVEUpdate):
    logger.info(f"Updating CVE {cve_id}")
    update_data = {k: v for k, v in cve_update.model_dump().items() if v is not None}
    return cves_collection.find_one_and_update(
        {"id": cve_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

def delete_cve(cve_id: str):
    logger.info(f"Deleting CVE {cve_id}")
    return cves_collection.find_one_and_delete({"cve_id": cve_id})
