from dataclasses import dataclass
from typing import List


@dataclass
class ScenarioUploadData:
    """
    Represents data for uploading a scenario.

    Attributes:
        parent_id : The ID of the parent scenario folder.
        model_id : The ID of the model associated with the scenario.
        folder_name ： The name of the folder containing the scenario files.
        file : The binary content of the scenario file.
    """

    parent_id: int
    model_id: int
    folder_name: str | None
    file: bytes | None

@dataclass
class ScenarioData:
    """
    Represents data for a scenario.

    Attributes:
        id ： The ID of the scenario.
        parent_id : The ID of the parent scenario folder.
        model_id : The ID of the model associated with the scenario.
        created : The creation timestamp of the scenario.
        path : The path of the scenario.
        children : The list of child scenario IDs.
    """

    id: int
    parent_id: int
    model_id: int
    created: str
    path: str
    children: List[str] | None


# TODO Currently not in use
class RunList:
    def __init__(self, name, description, runtime_configuration, model_id):
        self.data = {
            "name": name,
            "description": description,
            "runtime_configuration": runtime_configuration,
            "model_id": model_id,
        }

    def get_data(self):
        return self.data


# TODO Currently not in use
class Policy:
    def __init__(self, name, description, model_id):
        self.data = {
            "name": name,
            "description": description,
            "model_id": model_id,
        }

    def get_data(self):
        return self.data


# TODO Currently not in use
class ModelData:
    def __init__(
        self,
        name,
        description,
        output_bucket,
        job_queue,
        job_definition,
        compute_environment,
        ecr_registry,
    ):
        self.data = {
            "name": name,
            "description": description,
            "output_bucket": output_bucket,
            "job_queue": job_queue,
            "job_definition": job_definition,
            "compute_environment": compute_environment,
            "ecr_registry": ecr_registry,
        }

    def get_data(self):
        return self.data
