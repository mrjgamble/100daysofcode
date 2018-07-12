import pytest
from groceries import Groceries, Item, DuplicateProduct, MaxCravingsReached

@pytest.fixture()
def empty_grocery_cart():

    cart = Groceries()

    yield cart

@pytest.fixture()
def stocked_grocery_cart(items_list):

    cart = Groceries(items_list)

    yield cart

@pytest.fixture()
def items_list():
    products = 'celery apples water coffee chicken pizza'.split()
    prices = [1, 4, 2, 5, 6, 4]
    cravings = False, False, False, False, False, True
    items = []

    for i in zip(products, prices, cravings):
        items.append(Item(*i))

    return items

def test_create_empty_cart(empty_grocery_cart):
    assert len(empty_grocery_cart) == 0
    assert empty_grocery_cart.due == 0

def test_create_loaded_cart(stocked_grocery_cart):

    assert len(stocked_grocery_cart) == 6
    assert stocked_grocery_cart.due == 22

    assert stocked_grocery_cart[0].product == 'celery'
    assert stocked_grocery_cart[0].price == 1
    assert stocked_grocery_cart[-1].product == 'pizza'
    assert stocked_grocery_cart[-1].price == 4
    assert stocked_grocery_cart.num_cravings_reached == False


def test_add_item(stocked_grocery_cart):

    oranges = Item(product='oranges', price=3, craving=False)
    stocked_grocery_cart.add(oranges)

    assert len(stocked_grocery_cart) == 7
    assert stocked_grocery_cart[-1].product == 'oranges'
    assert stocked_grocery_cart[-1].price == 3
    assert stocked_grocery_cart.due == 25
    assert stocked_grocery_cart.num_cravings_reached == False

def test_add_item_duplicate(stocked_grocery_cart):

    apples = Item(product='apples', price=4, craving=False)

    with pytest.raises(DuplicateProduct):
        stocked_grocery_cart.add(apples)

def test_add_item_max_cravings(stocked_grocery_cart):

    chocolate = Item(product='chocolate', price=2, craving=True)
    butter_tart = Item(product='butter tart', price=1, craving=True)

    stocked_grocery_cart.add(chocolate)
    assert stocked_grocery_cart.num_cravings_reached == True

    with pytest.raises(MaxCravingsReached):
        stocked_grocery_cart.add(butter_tart)

def test_delete_item(stocked_grocery_cart):

    chocolate = Item(product='chocolate', price=2, craving=True)

    with pytest.raises(IndexError):
        stocked_grocery_cart.delete(chocolate)

    assert len(stocked_grocery_cart) == 6
    stocked_grocery_cart.delete('apples')
    assert len(stocked_grocery_cart) == 5

    assert len(list(stocked_grocery_cart.search('apples'))) == 0

@pytest.mark.parametrize('test_input, expected',
                         [('banana', 0),
                         ('water', 1),
                         ('Apples', 1),
                         ('apple', 1),
                         ('le', 2),
                         ('zZ', 1),
                         ('e', 5)])
def test_search_item(test_input, expected, stocked_grocery_cart):
    assert len(list(stocked_grocery_cart.search(test_input))) == expected
