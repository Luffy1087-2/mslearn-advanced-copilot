from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_region_cities():
    """Return the cities for a known region."""
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_unknown_region():
    """Return the agreed not-found response for an unknown region."""
    response = client.get("/regions/Unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Region not found"


def test_post_region_cities_not_allowed():
    """Reject POST requests to the region city-list route."""
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_region_route_in_openapi():
    """Include the region city-list route in the generated OpenAPI schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/regions/{region}" in response.json()["paths"]


def test_monthly_weather_response():
    """Keep both monthly weather routes returning the same dataset values."""
    existing_response = client.get("/countries/Spain/Seville/January")
    assert existing_response.status_code == 200
    assert existing_response.json() == {"high": 61, "low": 41}

    response = client.get("/regions/Spain/Seville/January")
    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}