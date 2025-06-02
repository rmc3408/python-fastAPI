from fastapi import status
from .setup import *
from ..routers.todos import get_current_user, get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all(test_todo):
    print("Running test_read_all...")

    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json() == [test_todo.to_dict()]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_todo.to_dict()


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo):
    body={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todo/', json=body)
    assert response.status_code == 201

    db = TestingSessionLocal()
    result = db.query(Todos).filter(Todos.id == 2).first()
    if result is None:
        pytest.fail("Todo with id 2 not found in the database.")
    
    assert result.title == body.get('title')
    assert result.description == body.get('description')
    assert result.priority == body.get('priority')


def test_update_todo(test_todo):
    request_data={
        'title':'Changed!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    result = db.query(Todos).filter(Todos.id == 1).first()
    if result is None:
        pytest.fail("Todo with id 1 not found in the database.")
    assert result.title == request_data['title']


def test_update_todo_not_found(test_todo):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete('/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

