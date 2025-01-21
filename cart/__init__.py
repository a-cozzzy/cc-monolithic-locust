import json

import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data):
        return cls(data['id'], data['username'], json.loads(data['contents']), data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Collect all product IDs from the cart details in one go
    product_ids = []
    for cart_detail in cart_details:
        product_ids.extend(json.loads(cart_detail['contents']))  # Parse JSON directly

    # Fetch all products in one call to reduce database/API calls
    products_list = get_products(product_ids)  # Fetch products based on collected IDs

    # Return the list of products directly
    return products_list


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)