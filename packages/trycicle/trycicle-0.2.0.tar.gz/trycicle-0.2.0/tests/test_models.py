import pytest

from trycicle.models import Config, Service
from trycicle.parser import parse_config


@pytest.fixture
def example() -> Config:
    with open("tests/example.yml") as fp:
        return parse_config(fp)


def test_get_all_parents(example: Config) -> None:
    parent_names = [
        "operator integration tests",
        ".tests",
        ".only module",
        ".install dev dependencies",
    ]
    all_parents = list(example.all_parents("operator integration tests"))

    defaults = all_parents.pop()
    assert defaults is example.defaults

    assert len(all_parents) == len(parent_names)
    for job, name in zip(all_parents, parent_names):
        assert job is example.jobs[name]


def test_resolve_field(example: Config) -> None:
    assert (
        example.resolve_field("operator integration tests", "image").name
        == "python:3.11"
    )
    assert "pipenv run ci-coverage -k integration" in example.resolve_field(
        "operator integration tests", "script"
    )


def test_resolve_field_not_set(example: Config) -> None:
    example.defaults.image = None
    with pytest.raises(KeyError, match="resolve field 'image'"):
        example.resolve_field("operator integration tests", "image")


def test_resolve_invalid_field(example: Config) -> None:
    with pytest.raises(AttributeError):
        example.resolve_field("operator integration tests", "invalid")


def test_merge_fields(example: Config) -> None:
    variables = example.merge_fields("operator integration tests", "variables")
    assert variables["MODULE"] == "operator"
    assert variables["AWS_ACCOUNT_ID"] == "123456"


def test_append_fields(example: Config) -> None:
    example.defaults.services = [Service("postgres:latest", "postgres")]
    services = example.append_fields("operator integration tests", "services")
    assert len(services) == 2
    assert all(isinstance(service, Service) for service in services)
    assert services[0].name == "docker:20-dind"
    assert services[1].name == "postgres:latest"


def test_get_job(example: Config) -> None:
    job = example.get_job("operator integration tests")
    assert job.image.name == "python:3.11"
    assert "pipenv install --deploy --dev" in job.before_script
    assert "pipenv run ci-coverage -k integration" in job.script
    assert job.variables["MODULE"] == "operator"
    assert job.services[0].name == "docker:20-dind"
