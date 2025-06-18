def test_request_main_page(client):
    """Test that the main page returns a 200 OK status."""
    response = client.get("/")
    assert response.status_code == 200
