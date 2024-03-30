import google.protobuf.message
import modal._output
import modal.client
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

_Function = typing.TypeVar("_Function")

class _LocalApp:
    _tag_to_object_id: typing.Dict[str, str]
    _client: modal.client._Client
    _app_id: str
    _app_page_url: str
    _environment_name: str
    _interactive: bool

    def __init__(self, client: modal.client._Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, environment_name: typing.Union[str, None] = None, interactive: bool = False):
        ...

    @property
    def client(self) -> modal.client._Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    @property
    def is_interactive(self) -> bool:
        ...

    async def _create_all_objects(self, indexed_objects: typing.Dict[str, modal.object._Object], new_app_state: int, environment_name: str, output_mgr: typing.Union[modal._output.OutputManager, None] = None):
        ...

    async def disconnect(self, reason: typing.Union[int, None] = None, exc_str: typing.Union[str, None] = None):
        ...

    async def stop(self):
        ...

    def log_url(self):
        ...

    @staticmethod
    async def _init_existing(client: modal.client._Client, existing_app_id: str) -> _LocalApp:
        ...

    @staticmethod
    async def _init_new(client: modal.client._Client, description: str, app_state: int, environment_name: str = '', interactive=False) -> _LocalApp:
        ...

    @staticmethod
    async def _init_from_name(client: modal.client._Client, name: str, namespace, environment_name: str = ''):
        ...

    async def deploy(self, name: str, namespace, public: bool) -> str:
        ...


class _ContainerApp:
    _client: typing.Union[modal.client._Client, None]
    _app_id: typing.Union[str, None]
    _environment_name: typing.Union[str, None]
    _tag_to_object_id: typing.Dict[str, str]
    _object_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]
    _is_interactivity_enabled: bool
    _function_def: typing.Union[modal_proto.api_pb2.Function, None]
    _fetching_inputs: bool

    def __init__(self):
        ...

    @property
    def client(self) -> typing.Union[modal.client._Client, None]:
        ...

    @property
    def app_id(self) -> typing.Union[str, None]:
        ...

    @property
    def fetching_inputs(self) -> bool:
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
    _tag_to_object_id: typing.Dict[str, str]
    _client: modal.client.Client
    _app_id: str
    _app_page_url: str
    _environment_name: str
    _interactive: bool

    def __init__(self, client: modal.client.Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, environment_name: typing.Union[str, None] = None, interactive: bool = False):
        ...

    @property
    def client(self) -> modal.client.Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    @property
    def is_interactive(self) -> bool:
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

    class __stop_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    stop: __stop_spec

    def log_url(self):
        ...

    class ___init_existing_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, existing_app_id: str) -> LocalApp:
            ...

        async def aio(self, *args, **kwargs) -> LocalApp:
            ...

    _init_existing: ___init_existing_spec

    class ___init_new_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, description: str, app_state: int, environment_name: str = '', interactive=False) -> LocalApp:
            ...

        async def aio(self, *args, **kwargs) -> LocalApp:
            ...

    _init_new: ___init_new_spec

    class ___init_from_name_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, name: str, namespace, environment_name: str = ''):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _init_from_name: ___init_from_name_spec

    class __deploy_spec(typing_extensions.Protocol):
        def __call__(self, name: str, namespace, public: bool) -> str:
            ...

        async def aio(self, *args, **kwargs) -> str:
            ...

    deploy: __deploy_spec


class ContainerApp:
    _client: typing.Union[modal.client.Client, None]
    _app_id: typing.Union[str, None]
    _environment_name: typing.Union[str, None]
    _tag_to_object_id: typing.Dict[str, str]
    _object_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]
    _is_interactivity_enabled: bool
    _function_def: typing.Union[modal_proto.api_pb2.Function, None]
    _fetching_inputs: bool

    def __init__(self):
        ...

    @property
    def client(self) -> typing.Union[modal.client.Client, None]:
        ...

    @property
    def app_id(self) -> typing.Union[str, None]:
        ...

    @property
    def fetching_inputs(self) -> bool:
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
