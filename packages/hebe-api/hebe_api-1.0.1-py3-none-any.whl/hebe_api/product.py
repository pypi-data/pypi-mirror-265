from .entity import Entity
from bs4.element import Tag


class Product(Entity):
    def __init__(self, row: Tag):
        title = row.find("div", class_="product-package__title")
        if title is None:
            raise Exception(
                f"Title not found for the product. Full tag: {row.text}"
            )
        self.title: str = self._remove_endlines(title.text)

        subtitle = row.find("div", class_="product-package__subtitle")
        if subtitle is None:
            raise Exception(
                f"Subtitle not found for the product. Full tag: {row.text}"
            )
        self.subtitle: str = self._remove_endlines(subtitle.text)

        [total_price, package_price] = row.find_all(
            "div", class_="price-package__amount"
        )
        self.total_price_str: str = self._remove_endlines(total_price.text)
        self.package_price_str: str = self._remove_endlines(package_price.text)
        self.total_price: float = self._price_to_float(self.total_price_str)
        self.package_price: float = self._price_to_float(
            self.package_price_str
        )

        [quantity] = row.find_all("div", class_="product-package__qty")
        self.quantity: int = int(quantity.text)

    def __repr__(self) -> str:
        return (
            f"Product({self.title}, {self.quantity}) - {self.total_price} PLN"
        )
