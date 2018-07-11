import app
import pytest

import json

BASE_URL = 'http://127.0.0.1:5000/api/v1.0/items'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)
BAD_URL = 'http://127.0.0.1:5000/noname'

@pytest.fixture(scope='session')
def test_client():
    """
    Create a flask test client, returning the client to each function as required
    """
    testing_client = app.app.test_client()
    testing_client.testing = True

    yield testing_client

@pytest.fixture(scope='function')
def item():
    """
    returns a valid item in the form of a dictionary
    """
    return {'name':'box',
            'value':340}

@pytest.fixture(scope='function')
def item_duplicate():
    """
    returns a duplicate item in the form of a dictionary
    """
    return {'name':'chair',
            'value':300}

@pytest.fixture(scope='function')
def item_without_name():
    """
    returns an item having no 'name' key
    """
    return {'value':340}

@pytest.fixture(scope='function')
def item_without_value():
    """
    returns an item having no 'value' key
    """
    return {'name':'box'}

@pytest.fixture(scope='function')
def item_with_bad_value():
    """
    returns an item having an invalid 'value'
    """
    return {'name':'box',
            'value':'thirty'}


def test_get_all_items(test_client):
    """
    GIVEN a flask application containing 3 items
    WHEN a user requests all items
    THEN check that all 3 items are returned to the user
    """

    response = test_client.get(BASE_URL)

    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert len(data['items']) == 3

def test_get_single_good_item(test_client):
    """
    GIVEN a flask application
    WHEN a user request a single item
    THEN check that a single item is returned with the expected ID
    """

    response = test_client.get(GOOD_ITEM_URL)

    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert len(data['items']) == 1
    assert data['items'][0]['id'] == 3

def test_get_single_bad_item(test_client):
    """
    GIVEN a flask application
    WHEN a user requests an item that does not exist
    THEN check that the correct code & response are returned
    """

    response = test_client.get(BAD_ITEM_URL)

    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert data['error'] == app.NOT_FOUND

def test_create_item_good(test_client, item):
    """
    GIVEN a flask application
    WHEN a user requests to create a new item
    THEN check that the item is successfully added to the db
    """

    response = test_client.post(BASE_URL,
                                data=json.dumps(item),
                                content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 201
    assert data['item']['name'] == item['name']
    assert data['item']['value'] == item['value']
    assert data['item']['id'] > 0

def test_create_item_missing_name(test_client, item_without_name):
    """
    GIVEN a flask application
    WHEN a user requests to create an item missing the 'name' variable
    THEN check that the task is not added to the database and that the appropriate response
    is returned
    """

    response = test_client.post(BASE_URL,
                                data=json.dumps(item_without_name),
                                content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_create_item_missing_value(test_client, item_without_value):
    """
    GIVEN a flask application
    WHEN a user requests to create an item missing the 'value' variable
    THEN check that bad request resposne is provided
    """

    response = test_client.post(BASE_URL,
                                data=json.dumps(item_without_value),
                                content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_create_item_duplicate_name(test_client, item_duplicate):
    """
    GIVEN a flask application
    WHEN a user adds an item with duplicate name
    THEN check that a bad request response is provided
    """

    response = test_client.post(BASE_URL,
                                data=json.dumps(item_duplicate),
                                content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_create_item_incorrect_value(test_client,item_with_bad_value):
    """
    GIVEN a flask application
    WHEN a user adds an item with incorrect value
    THEN check that a bad request response is provided
    """

    item = {'name':'table top', 'value':'thirty'}

    response = test_client.post(BASE_URL,
                                data=json.dumps(item_with_bad_value),
                                content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_update_item_good(test_client, item):
    """
    GIVEN a flask application
    WHEN a user updates a valid item
    THEN check that a valid response is provided
    """

    response = test_client.put(GOOD_ITEM_URL,
                                  data=json.dumps(item),
                                  content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert data['item']['name'] == item['name']
    assert data['item']['value'] == item['value']

def test_update_item_incorrect_id(test_client, item):
    """
    GIVEN a flask application
    WHEN a user updates a non existent item id
    THEN check that a valid 404 response is provided
    """

    response = test_client.put(BAD_ITEM_URL,
                               data=json.dumps(item),
                               content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert data['error'] == app.NOT_FOUND

def test_update_item_incorrect_content_type(test_client, item):
    """
    GIVEN a flask applicatin
    WHEN a user updates an item, providing an incorrect content type
    THEN check that a valid 400 response is provided
    """

    response = test_client.put(GOOD_ITEM_URL,
                               data=json.dumps(item))

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_update_item_incorrect_value_type(test_client, item_with_bad_value):
    """
    GIVEN a flask application
    WHEN a user updates an item, providing an incorrect value type
    THEN check that a valid 400 response is provided
    """

    response = test_client.put(GOOD_ITEM_URL,
                               data=json.dumps(item_with_bad_value),
                               content_type='application/json')

    data = json.loads(response.get_data())

    assert response.status_code == 400
    assert data['error'] == app.BAD_REQUEST

def test_delete_item(test_client):
    """
    GIVEN a flask application
    WHEN a user deletes an item
    THEN provide a valid status code to confirm delete
    """

    response = test_client.delete(GOOD_ITEM_URL)

    assert response.status_code == 204
    assert response.get_data() == b''

def test_delete_item_incorrect_id(test_client):
    """
    GIVEN a flask application
    WHEN a user deletes an item that does not exist
    THEN check that a valid 404 response is provided
    """

    response = test_client.delete(GOOD_ITEM_URL)

    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert data['error'] == app.NOT_FOUND

