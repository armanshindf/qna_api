def test_create_answer(client):
    question_response = client.post("/questions/", json={"text": "Test question?"})
    question_id = question_response.json()["id"]
    
    answer_data = {
        "text": "Test answer",
        "user_id": "user_123"
    }
    response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
    assert response.status_code == 201
    assert response.json()["text"] == "Test answer"

def test_create_answer_nonexistent_question(client):
    answer_data = {
        "text": "Test answer",
        "user_id": "user_123"
    }
    response = client.post("/questions/999/answers/", json=answer_data)
    assert response.status_code == 404