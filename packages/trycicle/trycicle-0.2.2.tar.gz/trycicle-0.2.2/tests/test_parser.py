import io

import pytest

from trycicle.models import Reference
from trycicle.parser import parse_config, parse_image, parse_service, resolve_references


def test_parse_config() -> None:
    with open("tests/example.yml") as fp:
        config = parse_config(fp)
    assert len(config.jobs) == 5
    assert "operator tests" in config.jobs
    assert "variables" not in config.jobs
    assert config.defaults.variables is not None
    assert config.defaults.variables["AWS_ACCOUNT_ID"] == "123456"


def test_parser_missing_defaults() -> None:
    config = parse_config(io.StringIO("{}"))
    assert config.defaults.variables == {}
    assert config.defaults.before_script == []
    assert config.defaults.services == []


def test_parser_defaults() -> None:
    config_file = io.StringIO(
        """\
variables:
  FOO: bar
before_script:
  - echo "Hello, world!"
services:
  - postgres:latest
"""
    )
    config = parse_config(config_file)
    assert config.defaults.variables == {"FOO": "bar"}
    assert config.defaults.before_script == ['echo "Hello, world!"']
    assert config.defaults.services is not None
    assert config.defaults.services[0].name == "postgres:latest"


def test_parse_service_from_string() -> None:
    service = parse_service("docker:20-dind")
    assert service.name == "docker:20-dind"
    assert service.alias == "docker"


def test_parse_service_alias() -> None:
    service = parse_service("tutum/wordpress:latest")
    assert service.alias == "tutum-wordpress"


def test_parse_service_dict() -> None:
    service = parse_service({"name": "docker:20-dind", "alias": "test"})
    assert service.name == "docker:20-dind"
    assert service.alias == "test"


def test_parse_service_with_command() -> None:
    service = parse_service({"name": "docker:20-dind", "command": "ls -la"})
    assert service.name == "docker:20-dind"
    assert service.alias == "docker"
    assert service.command == ["ls", "-la"]


def test_parse_service_with_command_list() -> None:
    service = parse_service({"name": "docker:20-dind", "command": ["ls", "-la"]})
    assert service.name == "docker:20-dind"
    assert service.command == ["ls", "-la"]


def test_parse_service_invalid() -> None:
    with pytest.raises(ValueError, match="Unable to parse service"):
        parse_service([])


def test_parse_image_from_string() -> None:
    image = parse_image("busybox:latest")
    assert image.name == "busybox:latest"
    assert image.entrypoint is None


def test_parse_image_from_dict() -> None:
    image = parse_image({"name": "busybox:latest"})
    assert image.name == "busybox:latest"
    assert image.entrypoint is None


def test_parse_image_with_entrypoint() -> None:
    image = parse_image({"name": "busybox:latest", "entrypoint": "sh"})
    assert image.name == "busybox:latest"
    assert image.entrypoint == ["sh"]


def test_parse_image_with_entrypoint_arguments() -> None:
    image = parse_image({"name": "busybox:latest", "entrypoint": ["/bin/sh", "-c"]})
    assert image.name == "busybox:latest"
    assert image.entrypoint == ["/bin/sh", "-c"]


def test_parse_image_invalid() -> None:
    with pytest.raises(ValueError, match="Unable to parse image"):
        parse_image([])


def test_resolve_references_nested_lists() -> None:
    raw = {
        "first": "one",
        "last": "four",
        "list": [Reference(["first"]), "two", "three"],
        "flatten": [Reference(["list"]), Reference(["last"])],
        "nested": [[Reference(["list"])], [Reference(["last"])]],
    }
    resolved = resolve_references(raw, raw)
    assert resolved["list"] == ["one", "two", "three"]
    assert resolved["flatten"] == ["one", "two", "three", "four"]
    assert resolved["nested"] == [["one", "two", "three"], ["four"]]


def test_parse_references_variables() -> None:
    with open("tests/references.yml") as fp:
        config = parse_config(fp)

    vars_one = config.get_job("test-vars-1")
    assert vars_one.variables == {
        "URL": "http://my-url.internal",
        "IMPORTANT_VAR": "the details",
    }

    vars_two = config.get_job("test-vars-2")
    assert vars_two.variables == {"MY_VAR": "the details"}


def test_parse_references_scripts() -> None:
    with open("tests/references.yml") as fp:
        config = parse_config(fp)

    nested = config.get_job("nested-references")
    assert nested.script == ['echo "ONE!"', 'echo "TWO!"', 'echo "THREE!"']
