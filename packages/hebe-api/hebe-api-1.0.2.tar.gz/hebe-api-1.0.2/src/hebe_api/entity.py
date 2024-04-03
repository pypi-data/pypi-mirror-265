class Entity:
    def _price_to_float(self, price: str) -> float:
        return float(price.replace(",", ".").replace(" zł", "").strip())

    def _remove_endlines(self, text: str) -> str:
        return text.replace("\n", "").strip()
