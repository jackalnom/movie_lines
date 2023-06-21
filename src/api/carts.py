from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


@router.post("/carts", tags=["cart"])
def create_cart():
    """ """

    return {"cart_id": 1}


@router.get("/carts/{cart_id}", tags=["cart"])
def get_cart(cart_id: int):
    """ """

    return {}


class CartItem(BaseModel):
    quantity: int


@router.put("/carts/{cart_id}/items/{item_sku}", tags=["cart"])
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    """ """

    # Handle case with invalid sku

    # Handle invalid quantity of sku

    return {"cart_id": 1}


@router.post("/carts/{cart_id}/checkout", tags=["cart"])
def checkout(cart_id: int):
    """ """

    return {"order_id": 1}
