import dataclasses
import typing
from collections import deque


@dataclasses.dataclass
class Reference:
    path: list[str]


@dataclasses.dataclass
class Service:
    name: str
    alias: str
    variables: dict[str, str] | None = None
    entrypoint: list[str] | None = None
    command: list[str] | None = None

    @property
    def is_docker_dind(self) -> bool:
        return self.name.startswith("docker:") and "dind" in self.name


@dataclasses.dataclass
class JobImage:
    name: str
    entrypoint: list[str] | None = None


@dataclasses.dataclass
class PartialJob:
    extends: list[str]
    image: JobImage | None = None
    before_script: list[str] | None = None
    script: list[str] | None = None
    variables: dict[str, str] | None = None
    services: list[Service] | None = None


@dataclasses.dataclass
class Job:
    name: str
    image: JobImage
    before_script: list[str]
    script: list[str]
    variables: dict[str, str]
    services: list[Service]


@dataclasses.dataclass
class Config:
    defaults: PartialJob
    jobs: dict[str, PartialJob]

    def all_parents(self, name: str) -> typing.Iterable[PartialJob]:
        jobs = deque([name])
        while jobs:
            job = self.jobs[jobs.popleft()]
            yield job
            jobs.extendleft(job.extends)
        yield self.defaults

    def resolve_field(self, name: str, field: str) -> typing.Any:
        for job in self.all_parents(name):
            if (value := getattr(job, field)) is not None:
                return value
        raise KeyError(f"Unable to resolve field {field!r} for job {name!r}")

    def merge_fields(self, name: str, field: str) -> dict[str, str]:
        merged: dict[str, str] = {}
        for job in self.all_parents(name):
            if values := getattr(job, field):
                for key, value in values.items():
                    merged.setdefault(key, str(value))
        return merged

    def append_fields(self, name: str, field: str) -> list[typing.Any]:
        merged = []
        for job in self.all_parents(name):
            if values := getattr(job, field):
                merged += values
        return merged

    def get_job(self, name: str) -> Job:
        return Job(
            name=name,
            image=self.resolve_field(name, "image"),
            before_script=self.resolve_field(name, "before_script"),
            script=self.resolve_field(name, "script"),
            variables=self.merge_fields(name, "variables"),
            services=self.append_fields(name, "services"),
        )
