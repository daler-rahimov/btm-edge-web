
def test_get_spin(client, superuser_token_headers):
    response = client.get("/api/v1/ball_thrower/power", headers=superuser_token_headers)
    assert response.status_code == 200