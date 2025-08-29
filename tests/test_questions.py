def test_create_question(client):
    response = client.post("/questions/", json={"text": "Test question?"})
    assert response.status_code == 201
    assert response.json()["text"] == "Test question?"

def test_get_questions(client):
    client.post("/questions/", json={"text": "Question 1?"})
    client.post("/questions/", json={"text": "Question 2?"})
    
    response = client.get("/questions/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_nonexistent_question(client):
    response = client.get("/questions/999")
    assert response.status_code == 404