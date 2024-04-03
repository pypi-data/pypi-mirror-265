from typing import Type
from typing_extensions import Self


class GitAIException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CorruptedRepoError(GitAIException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    @classmethod
    def corrupted_uncommited_config(cls: Type[Self]) -> Self:
        return cls("The repository folder has an uncommited configuration file.")

    @classmethod
    def corrupted_commited_config(cls: Type[Self]) -> Self:
        return cls("The repository folder already has a commited configuration file.")


class RecursiveModuleError(GitAIException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    @classmethod
    def detected_recursive_module(cls: Type[Self], module_path: str, uri: str, commit: str) -> Self:
        return cls(f"The input folder at '{module_path}' pointing to {uri}:{commit}." % (module_path, uri, commit))


class CommandError(GitAIException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    @classmethod
    def unknown_ai_command(cls: Type[Self]) -> Self:
        return cls("Unknown AI command.")


class InitError(GitAIException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    @classmethod
    def failed_to_init_repo(cls: Type[Self]) -> Self:
        return cls("Failed to initialize Git AI repository.")

    @classmethod
    def repository_already_initialized(cls: Type[Self]) -> Self:
        return cls("Repository already initialized with Git AI. Please run `git ai init`.")


class ExperimentError(GitAIException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    @classmethod
    def repository_not_initialized(cls: Type[Self]) -> Self:
        return cls("Repository has not be initialized with Git AI. Please run `git ai init`")

    @classmethod
    def failed_to_start_experiment(cls: Type[Self]) -> Self:
        return cls("Failed to start experiment. Check if the repository is clean and the experiment branch does not exist.")

    @classmethod
    def failed_to_push_experiment(cls: Type[Self]) -> Self:
        return cls("Failed to push experiment branch. Check if the remotes are valid.")

    @classmethod
    def experiment_already_started(cls: Type[Self]) -> Self:
        return cls("Experiment already started but not closed. Please close the current experiment before starting a new one.")


class MetricError(GitAIException):
    @classmethod
    def unknown_data_type_enum(cls: Type[Self], data_type: str) -> Self:
        return cls(f"Unknown data type '{data_type}' for DataTypeEnum")
