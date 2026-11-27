"""Integration tests for the nginx service."""

from hamcrest import assert_that, contains_string, has_entries, has_properties
from httpx import Client


def test_nginx_redirects_http_to_https(nginx_service):
    with Client(base_url=f"http://{nginx_service.ip}") as client:
        response = client.get("/api/status")

    assert_that(response, has_properties(
        status_code=301,
        headers=has_entries(location=f"https://{nginx_service.ip}/api/status"),
    ))


def test_nginx_proxies_api(nginx_client):
    response = nginx_client.get("/api/status")

    assert_that(response, has_properties(
        status_code=200,
        headers=has_entries({"content-type": "application/json"}),
    ))


def test_nginx_proxies_frontend(nginx_client):
    response = nginx_client.get("/")

    assert_that(response, has_properties(
        status_code=200,
        headers=has_entries({"content-type": contains_string("text/html")}),
    ))


def test_nginx_status(nginx_client):
    response = nginx_client.get("/nginx_status")

    assert_that(response, has_properties(
        status_code=200,
        text=contains_string("Active connections"),
    ))
