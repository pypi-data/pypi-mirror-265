
from abfy.src.models.configuration_model.base_objects import SuperEnum


class Source(SuperEnum):
    validation = "validation"
    transformation = "transformation"
    analysis = "analysis"


class Status(SuperEnum):
    success = "success"
    fail = "fail"
    warn = "warn"
    skip = "skip"
