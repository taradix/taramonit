"""Service fixtures."""

import sys
from functools import partial

import pytest
from httpx import Client
from pytest_xdocker.compose import ComposeServer, find_compose_files


@pytest.fixture(scope="session")
def env_vars():
    """Environment variables for the services."""
    v = sys.version_info
    python_version = f"{v.major}.{v.minor}.{v.micro}"

    return {
        "PYTHON_VERSION": python_version,
        "SERVER_HOSTNAME": "test.local",
    }


@pytest.fixture(scope="session")
def env_file(env_vars, request):
    """Environment file containing `env_vars`.

    Cached for troubleshooting purposes.
    """
    env_file = request.config.cache.makedir("taramonit") / "env"
    with env_file.open("w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    return env_file


@pytest.fixture(scope="session")
def compose_server(env_file, process, request):
    return partial(
        ComposeServer,
        env_file=env_file,
        compose_files=find_compose_files(request.config.rootdir),
        process=process,
    )


@pytest.fixture(scope="session")
def nginx_service(compose_server):
    """Nginx service fixture."""
    server = compose_server("start worker process")
    with server.run("nginx") as service:
        yield service


@pytest.fixture
def nginx_client(nginx_service):
    """Client to the nginx service fixture, over the self-signed dev cert."""
    url = f"https://{nginx_service.ip}"
    with Client(base_url=url, timeout=5.0, verify=False) as client:  # noqa: S501
        yield client
