import importlib
import json
import os
import sys
from typing import Optional

import typer
from typing_extensions import Annotated

from service_sdk.client import Client
from service_sdk.service import Service, DEFAULT_SERVICE_HOST, DEFAULT_SERVICE_PORT

cli = typer.Typer()


@cli.command()
def run(
        work_dir: Annotated[str, typer.Option("--dir", "-d")] = None,
        import_path: Annotated[str, typer.Option("--import", "-i")] = "main",
        host: Annotated[str, typer.Option("--host", "-h")] = DEFAULT_SERVICE_HOST,
        port: Annotated[str, typer.Option("--port", "-p")] = DEFAULT_SERVICE_PORT
):
    if work_dir:
        sys.path.append(work_dir)

    import_path_list = import_path.split(":")
    module_path = import_path_list[0]
    entry_function = "main"
    if len(import_path_list) == 2:
        entry_function = import_path_list[1]
    elif len(import_path_list) > 2:
        raise ValueError(f"Too many ':' separators in {import_path}")

    module = None
    try:
        module = importlib.import_module(module_path)
    except ImportError:
        raise ImportError(f"Failed to import '{module_path}' from '{work_dir or os.getcwd()}'")
    try:
        func = getattr(module, entry_function)
    except AttributeError:
        raise ValueError(f"Function '{entry_function}' not found on {module=}")

    service = Service(worker_callback=func, host=host, port=port)
    service.run()


@cli.command()
def ping(host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).ping()
    print(result)


@cli.command("exit")
def exit_service(
        host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT, force: Optional[bool] = None, wait: Optional[bool] = None
):
    result = Client(host=host, port=port).exit(force=force, wait=wait)
    print(result)


@cli.command()
def stop_all(
        host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT, force: Optional[bool] = None, wait: Optional[bool] = None
):
    Client(host=host, port=port).stop_all(force=force, wait=wait)


@cli.command()
def start(
        host: str = DEFAULT_SERVICE_HOST,
        port: str = DEFAULT_SERVICE_PORT,
        name: Optional[str] = None,
        data: Optional[str] = None
):
    data = json.loads(data) if data else None
    result = Client(host=host, port=port).start_worker(name=name, data=data)
    print(result)


@cli.command()
def stop(uid: str, host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).stop_worker(uid=uid)
    print(result)


if __name__ == "__main__":
    cli()
