import shlex
import typing

import yaml

from .models import Config, JobImage, PartialJob, Reference, Service

NOT_JOBS = {"variables", "services", "workflow"}

T = typing.TypeVar("T")


def get_list(v: T | list[T]) -> list[T]:
    if isinstance(v, list):
        return v
    return [v]


def get_list_or_none(v: T | list[T] | None) -> list[T] | None:
    if isinstance(v, list):
        return v
    return [v] if v is not None else None


def parse_command(raw: str | list[str] | None) -> list[str] | None:
    if raw is None:
        return None
    return shlex.split(raw) if isinstance(raw, str) else raw


def parse_service(raw: typing.Any) -> Service:
    if isinstance(raw, str):
        raw = {"name": raw}
    if isinstance(raw, dict):
        alias, _, _ = raw["name"].replace("/", "-").partition(":")
        return Service(
            name=raw["name"],
            alias=raw.get("alias") or alias,
            variables=raw.get("variables"),
            entrypoint=parse_command(raw.get("entrypoint")),
            command=parse_command(raw.get("command")),
        )
    raise ValueError(f"Unable to parse service, expected str or dict, got {raw!r}")


def parse_image(raw: typing.Any) -> JobImage:
    if isinstance(raw, str):
        return JobImage(name=raw)
    if isinstance(raw, dict):
        if "entrypoint" in raw:
            raw["entrypoint"] = get_list_or_none(raw["entrypoint"])
        return JobImage(**raw)
    raise ValueError(f"Unable to parse image, expected str or dict, got {raw!r}")


def parse_job(raw: dict[str, typing.Any]) -> PartialJob:
    extends = get_list(raw.get("extends", []))
    image = parse_image(raw["image"]) if "image" in raw else None
    before_script: list[str] | None = get_list_or_none(raw.get("before_script"))
    script: list[str] | None = get_list_or_none(raw.get("script"))
    variables = raw.get("variables")
    if raw_services := raw.get("services"):
        services = [parse_service(s) for s in raw_services]
    else:
        services = None
    return PartialJob(
        extends=extends,
        image=image,
        before_script=before_script,
        script=script,
        variables=variables,
        services=services,
    )


def resolve_references(root: dict[str, typing.Any], value: typing.Any) -> typing.Any:
    if isinstance(value, Reference):
        resolved = root
        for key in value.path:
            resolved = resolved[key]
        return resolve_references(root, resolved)

    if isinstance(value, dict):
        return {k: resolve_references(root, v) for k, v in value.items()}

    if isinstance(value, list):
        new_value = []
        for item in value:
            # Flatten references that resolve to another list, but not nested lists
            resolved = resolve_references(root, item)
            if isinstance(item, Reference) and isinstance(resolved, list):
                new_value.extend(resolved)
            else:
                new_value.append(resolved)

        return new_value

    return value


class Loader(yaml.SafeLoader):
    def construct_reference(self, node: yaml.SequenceNode) -> Reference:
        return Reference(self.construct_sequence(node))


Loader.add_constructor("!reference", Loader.construct_reference)


def parse_config(fp: typing.TextIO) -> Config:
    raw = yaml.load(fp, Loader)

    assert isinstance(raw, dict)
    raw = resolve_references(raw, raw)

    defaults = parse_job(raw)
    if defaults.before_script is None:
        defaults.before_script = []
    if defaults.variables is None:
        defaults.variables = {}
    if defaults.services is None:
        defaults.services = []

    jobs = {}
    for key, maybe_job in raw.items():
        if isinstance(maybe_job, dict) and key not in NOT_JOBS:
            jobs[key] = parse_job(maybe_job)

    return Config(defaults=defaults, jobs=jobs)
