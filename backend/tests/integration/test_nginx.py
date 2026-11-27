"""Integration tests for the nginx service."""

from httpx import Client


def test_nginx_redirects_http_to_https(nginx_service):
    with Client(base_url=f"http://{nginx_service.ip}") as client:
        response = client.get("/api/status")

    assert response.status_code == 301
    assert response.headers["location"] == f"https://{nginx_service.ip}/api/status"


def test_nginx_proxies_api(nginx_client):
    response = nginx_client.get("/api/status")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_nginx_proxies_frontend(nginx_client):
    response = nginx_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_nginx_status(nginx_client):
    response = nginx_client.get("/nginx_status")

    assert response.status_code == 200
    assert "Active connections" in response.text
