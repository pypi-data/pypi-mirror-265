from .order import Order
from .product import Product
import requests
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup


class Hebe:
    NO_TOKEN = "Use hebe.authenticate() in order to obtain the token"
    BASE_URL = "https://www.hebe.pl"

    def __init__(self, username: str = "", password: str = "") -> None:
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self, username: str = "", password: str = "") -> None:
        if username != "":
            self.username = username
        if password != "":
            self.password = password
        initial_token, csrf_token = self._get_initial_token()
        self.token = self._authenticate(initial_token, csrf_token)

    def _authenticate(self, initial_token: str, csrf_token: str) -> str:
        url = (
            f"{self.BASE_URL}/on/demandware.store/Sites-Hebe-Site"
            "/en_US/Login-LoginForm"
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/home?showform=true"
            "&targeturl=%2Faccount",
            "Cookie": f"dwsid={initial_token};",
        }
        body = urlencode(
            {
                "dwfrm_login_username_d0uexrwjfbur": self.username,
                "dwfrm_login_password_d0vyhxgwmmwx": self.password,
                "csrf_token": csrf_token,
                "dwfrm_login_login": "",
                "format": "ajax",
            }
        )
        response = requests.post(url=url, headers=headers, data=body)
        response_data = json.loads(response.text)
        if "error" in response_data:
            raise Exception(f"Authentication failed: {response_data['error']}")
        elif (
            "status" not in response_data
            or response_data["status"] != "SUCCESS"
        ):
            raise Exception(
                "Authentication failed: lack of 'status'='SUCCESS' flag"
                "in authenticate response body"
            )
        header = response.headers["Set-Cookie"]
        if "dwsid=" not in header:
            raise Exception(
                "dwsid cookie is not present in the final token retrieval"
            )
        dwsid = header.split("dwsid=")[1].split(";")[0]
        if not dwsid:
            raise Exception(
                "dwsid cookie missing. Please contact the "
                "author of the lib for resolution"
            )
        return dwsid

    def get_order_products(self, order: Order) -> list[Product]:
        if self.token is None:
            raise Exception(self.NO_TOKEN)
        return self._get_order_products(order)

    def _get_order_products(self, order: Order) -> list[Product]:
        url = (
            f"{self.BASE_URL}/on/demandware.store/Sites-Hebe-Site"
            "/en_US/Order-Orders"
        )
        key = f"dwfrm_orders_orderlist_i{order.position}_show"
        val = "POKA%C5%BB+SZCZEG%C3%93%C5%81Y"
        body = urlencode({key: val})
        response = requests.post(url, headers=self.headers(), data=body)
        if response.status_code != 200:
            raise Exception(
                "Response status code for retrieving"
                f"products was {response.status_code}."
                " Expected 200."
            )
        txt = response.text
        soup = BeautifulSoup(txt, "html.parser")
        product_package_rows = soup.find_all(
            "div", class_="product-package__row"
        )[1:]

        return [Product(row) for row in product_package_rows]

    def get_orders(self, start: int = 0, max_orders: int = 100) -> list[Order]:
        if self.token is None:
            raise Exception(self.NO_TOKEN)
        return self._get_orders(start, max_orders)

    def get_all_products(self, max_orders: int = 100) -> list[Product]:
        orders = self.get_orders(max_orders=max_orders)
        products: list[Product] = []
        for order in orders:
            products.extend(self.get_order_products(order))
        return products

    def _get_orders(
        self, start: int, max_orders: int = 100, orders: list[Order] = []
    ):
        url = f"{self.BASE_URL}/orders?order_status=1&start={start}"
        response = requests.get(url, headers=self.headers())
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve orders. Status code:"
                f"{response.status_code}"
            )
        txt = response.text
        if "orders-detail__section" not in txt:
            raise Exception(
                "Failed to retrieve orders. Missing"
                " orders-detail__section div class. Please ensure"
                " you have at least 1 order in your account."
            )
        soup = BeautifulSoup(txt, "html.parser")
        orders_details_section = soup.find_all(
            "div", class_="orders-detail__section"
        )
        orders.extend(
            [
                Order(order_section, i + start)
                for i, order_section in enumerate(orders_details_section)
            ]
        )
        if len(orders_details_section) == 5 and len(orders) < max_orders:
            self._get_orders(start + 5, max_orders, orders)

        return orders

    def _get_initial_token(self) -> tuple[str, str]:
        response = requests.get(self.BASE_URL)
        header = response.headers["Set-Cookie"]
        if "dwsid=" not in header:
            raise Exception(
                "dwsid cookie is not present in the initial token retrieval"
            )
        dwsid = header.split("dwsid=")[1].split(";")[0]
        if not dwsid:
            raise Exception(
                "dwsid cookie missing. Please contact the "
                "author of the lib for resolution"
            )
        csrf_json = json.loads(
            response.text.split("window.CSRFToken = ")[1].split(";")[0]
        )
        csrf_token = csrf_json["value"]
        return dwsid, csrf_token

    def headers(self):
        return {
            "Cookie": f"dwsid={self.token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
