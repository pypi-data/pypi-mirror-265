import google.protobuf.message
import modal._output
import modal.client
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

_Function = typing.TypeVar("_Function")

class _LocalApp:
    tag_to_object_id: typing.Dict[str, str]
    client: modal.client._Client
    app_id: str
    app_page_url: str
    environment_name: str
    interactive: bool

    def __init__(self, client: modal.client._Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, environment_name: typing.Union[str, None] = None, interactive: bool = False):
        ...

    async def _create_all_objects(self, indexed_objects: typing.Dict[str, modal.object._Object], new_app_state: int, environment_name: str, output_mgr: typing.Union[modal._output.OutputManager, None] = None):
        ...

    async def disconnect(self, reason: typing.Union[int, None] = None, exc_str: typing.Union[str, None] = None):
        ...


class _ContainerApp:
    client: typing.Union[modal.client._Client, None]
    app_id: typing.Union[str, None]
    environment_name: typing.Union[str, None]
    tag_to_object_id: typing.Dict[str, str]
    object_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]
    is_interactivity_enabled: bool
    function_def: typing.Union[modal_proto.api_pb2.Function, None]
    fetching_inputs: bool

    def __init__(self):
        ...

    def associate_stub_container(self, stub):
        ...

    def _has_object(self, tag: str) -> bool:
        ...

    def _hydrate_object(self, obj, tag: str):
        ...

    def hydrate_function_deps(self, function: _Function, dep_object_ids: typing.List[str]):
        ...

    async def init(self, client: modal.client._Client, app_id: str, environment_name: str = '', function_def: typing.Union[modal_proto.api_pb2.Function, None] = None):
        ...

    @staticmethod
    def _reset_container():
        ...

    def stop_fetching_inputs(self):
        ...


class LocalApp:
    tag_to_object_id: typing.Dict[str, str]
    client: modal.client.Client
    app_id: str
    app_page_url: str
    environment_name: str
    interactive: bool

    def __init__(self, client: modal.client.Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, environment_name: typing.Union[str, None] = None, interactive: bool = False):
        ...

    class ___create_all_objects_spec(typing_extensions.Protocol):
        def __call__(self, indexed_objects: typing.Dict[str, modal.object.Object], new_app_state: int, environment_name: str, output_mgr: typing.Union[modal._output.OutputManager, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _create_all_objects: ___create_all_objects_spec

    class __disconnect_spec(typing_extensions.Protocol):
        def __call__(self, reason: typing.Union[int, None] = None, exc_str: typing.Union[str, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    disconnect: __disconnect_spec


class ContainerApp:
    client: typing.Union[modal.client.Client, None]
    app_id: typing.Union[str, None]
    environment_name: typing.Union[str, None]
    tag_to_object_id: typing.Dict[str, str]
    object_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]
    is_interactivity_enabled: bool
    function_def: typing.Union[modal_proto.api_pb2.Function, None]
    fetching_inputs: bool

    def __init__(self):
        ...

    def associate_stub_container(self, stub):
        ...

    def _has_object(self, tag: str) -> bool:
        ...

    def _hydrate_object(self, obj, tag: str):
        ...

    def hydrate_function_deps(self, function: _Function, dep_object_ids: typing.List[str]):
        ...

    class __init_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, app_id: str, environment_name: str = '', function_def: typing.Union[modal_proto.api_pb2.Function, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    init: __init_spec

    @staticmethod
    def _reset_container():
        ...

    def stop_fetching_inputs(self):
        ...


_container_app: _ContainerApp

container_app: ContainerApp

async def _interact(client: typing.Union[modal.client._Client, None] = None) -> None:
    ...


class __interact_spec(typing_extensions.Protocol):
    def __call__(self, client: typing.Union[modal.client.Client, None] = None) -> None:
        ...

    async def aio(self, *args, **kwargs) -> None:
        ...

interact: __interact_spec


def is_local() -> bool:
    ...


async def _list_apps(env: str, client: typing.Union[modal.client._Client, None] = None) -> typing.List[modal_proto.api_pb2.AppStats]:
    ...


class __list_apps_spec(typing_extensions.Protocol):
    def __call__(self, env: str, client: typing.Union[modal.client.Client, None] = None) -> typing.List[modal_proto.api_pb2.AppStats]:
        ...

    async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.AppStats]:
        ...

list_apps: __list_apps_spec
