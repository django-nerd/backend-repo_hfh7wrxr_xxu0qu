"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Core user schema example (kept for reference/demo)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

# CCTV shop specific schemas
class CCTVProduct(BaseModel):
    """
    CCTV products collection
    Collection name: "cctvproduct"
    """
    title: str = Field(..., description="Product title")
    brand: str = Field(..., description="Brand name")
    model: Optional[str] = Field(None, description="Model identifier")
    category: str = Field(..., description="Category e.g. Camera, DVR, NVR, Kit, Accessory")
    price: float = Field(..., ge=0, description="Price in dollars")
    in_stock: bool = Field(True, description="Whether product is in stock")
    resolution: Optional[str] = Field(None, description="Resolution such as 1080p, 4MP, 4K")
    camera_type: Optional[str] = Field(None, description="Type such as Bullet, Dome, PTZ, Turret")
    channels: Optional[int] = Field(None, description="For recorders: number of channels")
    features: List[str] = Field(default_factory=list, description="Key features list")
    image_url: Optional[str] = Field(None, description="Primary image URL")
    images: List[str] = Field(default_factory=list, description="Additional image URLs")
    description: Optional[str] = Field(None, description="Long description")

class Inquiry(BaseModel):
    """
    Customer inquiries/quotes
    Collection name: "inquiry"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    message: Optional[str] = None
    items: List[dict] = Field(default_factory=list, description="Cart items at time of inquiry")

# Backwards-compatible generic product (not used by app, but kept for examples)
class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
