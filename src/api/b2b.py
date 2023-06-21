from fastapi import APIRouter
from enum import Enum
from pydantic import BaseModel

router = APIRouter()


class PotionInventory(BaseModel):
    red_amount: int
    blue_amount: int
    green_amount: int

    quantity: int


# Taxes? Pay 20% of profit if records aren't kept. If records are
# accurate than pay 10% of profit.
class Audit(BaseModel):
    gold: int
    liters_red: int
    liters_blue: int
    liters_green: int
    potions: list[PotionInventory]


# Gets called every other day
@router.post("/b2b/auditor", tags=["b2b"])
def post_audit(audit: Audit):
    """ """

    return "OK"


class PotionEnum(str, Enum):
    red = "red"
    blue = "blue"
    green = "green"


class Barrel(BaseModel):
    sku: str

    liters_per_barrel: int
    color: PotionEnum
    price: int

    quantity: int


class WholesaleCatalog(BaseModel):
    barrels: list[Barrel]


# Gets called once a day
@router.post("/b2b/wholesaler", tags=["b2b"])
def post_wholesale_purchase_plan(wholesale_catalog: WholesaleCatalog):
    """ """

    return [
        {
            "sku": "blah",
            "quantity": 5,
        },
        {
            "sku": "blah",
            "quantity": 5,
        },
    ]
    # Initial logic: buy number of small red barrels equal to
    #  money / cost of small red barrels.


@router.post("/b2b/deliver_bottles", tags=["b2b"])
def post_deliver_bottles(potions_delivered: list[PotionInventory]):
    """ """

    return "OK"


# Gets called 4 times a day
@router.post("/b2b/bottler", tags=["b2b"])
def post_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.

    return {
        "bottling": [
            {
                "red": 100,
                "blue": 0,
                "green": 0,
                "quantity": 5,
            }
        ]
    }
