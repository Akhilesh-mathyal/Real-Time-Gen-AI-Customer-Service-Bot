import app as application

def test_home_page_loads():
    response = application.app.test_client().get("/")
    assert response.status_code == 200
    assert b"Customer support" in response.data

def test_message_is_required():
    response = application.app.test_client().post("/api/chat/stream", json={})
    assert response.status_code == 400

def test_demo_chat_stream(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = application.app.test_client().post("/api/chat/stream", json={"message":"What is the return policy?", "history":[]})
    body = response.data.decode()
    assert response.status_code == 200
    assert "event: token" in body
    assert "30 days" in body
