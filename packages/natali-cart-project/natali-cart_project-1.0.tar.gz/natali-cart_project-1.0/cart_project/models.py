# Item
# Cart

class Item:
    """
    Товар для роболти магазину

    :param name: Назва товару
    :type name:str
    :pafam description: Опис товару
    :type description:str
    :param price: Ціна товару
    :type price:float
    """
    def __init__(self,
                 name:str,
                 description:str,
                 price:float):
        self.name = name
        self.description = description
        self.price = price

    def show(self):
        """
        Метод відображення документації про товар
        """
        print(f"""Назва товару: {self.name}
Опис товару: {self.description}
Ціна товару: {self.price}""")

class Cart:
    """
    Корзина для магазину

    :param items: Товари у корзині
    :type items: list
    """
    def __init__(self):
        self.items = []
    def get_count(self):
        return len(self.items)
        """
        Метод вираховує кількість товарів у корзині
    
        :return: Повертаємо кількість товарів
        :rtype:int
        """
    def get_price(self):
        """
        Метод для підрахування вартості товарів

        :return: Повертаємо вартість товарів
        :rtype:int|float
        """
        price = 0
        for item in self.items:
            price += item.price
