"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def deal_product():
    return Product("rent", 15, "This is rent a book", 1000)


@pytest.fixture()
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0)
        assert product.check_quantity(999)
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        product.buy(100)
        assert product.quantity >= 0
        # TODO напишите проверки на метод buy

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        # Необходимо проверить вывод Исключения ValueError в тех случаях, когда количества товара не хватает в корзине
        # https://pytest-docs-ru.readthedocs.io/ru/latest/assert.html
        with pytest.raises(ValueError):
            product.buy(10000)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_adding_product_in_cart(self, cart, product, deal_product):
        # Проверяем добавление нового товара в корзину. Проверяем, что в корзине находится одно наименование.
        # Проверяем, что количество Продукта равно количеству добавленной продукции (т.к. изначально 0)

        cart.add_product(product, 10)
        assert len(cart.products) == 1
        assert cart.products[product] == 10

        # Проверяем, что добавление нового количества уже добавленного артикула увеличивает количество изделий,
        # но не артикулов

        cart.add_product(product, 15)
        assert len(cart.products) == 1
        assert cart.products[product] == 25

        # Проверяем, что добавление нового артикула добавляет новый товар с его количеством в корзину.
        # Проверяем, что количество нового товара равно количеству добавленной продукции.
        # Проверяем, что количество товара 1 не изменилось.
        # Проверяем, что увеличилось количество артикулов

        cart.add_product(deal_product, 15)

        assert cart.products[deal_product] == 15
        assert cart.products[product] == 25
        assert len(cart.products) == 2

    def test_remove_product_from_cart(self, product, cart):
        # Проверяем, что корзина очищается от товара, если не передается количество товара

        cart.add_product(product)
        cart.remove_product(product)
        assert product not in cart.products

        # Проверяем, что корзина очищается от товара, если мы удаляем товара больше, чем у нас было добавлено

        cart.add_product(product, 5)
        cart.remove_product(product, 6)
        assert product not in cart.products

        # Проверяем, что корзина очищается от такого количества товара, сколько было выбрано

        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert cart.products.get(product) is None

        # Проверяем, что корзина очищается от такого количества товара, сколько было выбрано

        cart.add_product(product, 5)
        cart.remove_product(product, 4)
        assert cart.products.get(product) == 1

    def test_clear_cart(self, deal_product, product, cart):
        # Проверяем, что корзина полностью очищается по команде (при наличии одного товара)
        cart.add_product(product, 5)
        cart.clear()
        assert cart.products.get(product) is None

        # Проверяем, что корзина полностью очищается по команде (при наличии нескольких товара)

        cart.add_product(product, 5)
        cart.add_product(deal_product, 5)
        cart.clear()
        assert cart.products.get(product) is None

    def test_get_total_price(self, deal_product, product, cart):
        # Проверяем, что итоговая стоимость равна сумме всех цен товаров в корзине (при наличии одного товара)

        cart.add_product(product, 5)
        assert cart.get_total_price() == 500  # 5 * 100

        # Проверяем, что итоговая стоимость равна сумме всех цен товаров в корзине (при наличии нескольких товара)

        cart.add_product(deal_product, 5)
        assert cart.get_total_price() == 575  # 15 * 5 + 100 * 5

    def test_buy(self, product, deal_product, cart):

        # Проверяем, что покупка доступного количества товара проходит успешно
        # Проверяем, что корзина очищается от купленных товаров

        cart.add_product(product, 5)
        cart.buy()
        assert not product.quantity == 0
        assert product.quantity == 995
        assert not cart.products

        # Проверяем, что покупка доступного количества товара проходит успешно (при нескольких товарах)
        # Проверяем, что корзина очищается от купленных товаров

        cart.add_product(product, 5)
        cart.add_product(deal_product, 5)
        cart.buy()
        assert not product.quantity == 0
        assert not deal_product.quantity == 0
        assert product.quantity == 990
        assert deal_product.quantity == 995
        assert not cart.products

        # Проверяем, что появится ошибка при попытке купить больше товара, чем есть на складе

        cart.add_product(product, 5000)
        with pytest.raises(ValueError):
            cart.buy()
