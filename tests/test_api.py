import json

def test_pi_verification_api(client):
    """Test the /math/api/verification/pi endpoint."""
    response = client.get("/math/api/verification/pi")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'plots' in data
    assert isinstance(data['plots'], dict)
    assert data['plots']['methods_comparison'].startswith('iVBORw0KGgo') # Check for PNG header in base64
