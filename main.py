import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import CCTVProduct, Inquiry

app = FastAPI(title="CCTV Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "CCTV Shop Backend Running"}


# Utility to convert Mongo documents
class MongoJSON(BaseModel):
    @staticmethod
    def to_json(doc):
        if not doc:
            return doc
        doc = dict(doc)
        if isinstance(doc.get("_id"), ObjectId):
            doc["id"] = str(doc.pop("_id"))
        return doc


@app.get("/api/products")
def list_products(category: Optional[str] = None, brand: Optional[str] = None, q: Optional[str] = None, limit: int = 50):
    filter_q = {}
    if category:
        filter_q["category"] = category
    if brand:
        filter_q["brand"] = brand
    if q:
        filter_q["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"features": {"$elemMatch": {"$regex": q, "$options": "i"}}},
        ]

    try:
        docs = get_documents("cctvproduct", filter_q, limit)
        return [MongoJSON.to_json(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products")
def create_product(product: CCTVProduct):
    try:
        inserted_id = create_document("cctvproduct", product)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inquiry")
def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"id": inserted_id, "message": "Inquiry received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
