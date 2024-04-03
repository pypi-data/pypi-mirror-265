from .entity import Entity
from bs4.element import Tag


class Order(Entity):
    def __init__(self, order_details_section: Tag, position: int):
        self.position = position
        self._tag = order_details_section
        [date, price, packs] = order_details_section.find_all(
            "span", class_="order-header__value"
        )
        self.date: str = date.text
        self.price_str: str = price.text
        self.price: float = self._price_to_float(self.price_str)
        self.packs: int = int(packs.text)
        [order_id] = order_details_section.find_all(
            "span", class_="order-header__number-value"
        )
        self.id: str = order_id.text

    def __repr__(self) -> str:
        return f"Order({self.id}, {self.position}): {self.date} - {self.price}"
