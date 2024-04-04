from typing import Union, Optional

import requests


class Client:
    def __init__(
            self,
            host: str = "127.0.0.1",
            port: Union[int, str] = 8080,
    ):
        self.host = host
        self.port = port
        self.conn_str = f"http://{host}:{port}"

    def get(self, path):
        response = requests.get(url=f"{self.conn_str}/{path}")
        return response.json()

    def post(self, path, data: Optional[dict] = None, params: Optional[dict] = None):
        response = requests.post(url=f"{self.conn_str}/{path}", json=data, params=params)
        return response.json()

    def ping(self):
        return self.get(path="")

    def exit(self, force: Optional[bool] = None, wait: Optional[bool] = None) -> str:
        params = {}
        if force is not None:
            params.update(dict(force=force))
        if wait is not None:
            params.update(dict(wait=force))
        try:
            self.post(path="exit", params=params)
            return "server is still up"
        except requests.exceptions.ConnectionError:
            return "server was stopped successfully"

    def stop_all(self, force: Optional[bool] = None, wait: Optional[bool] = None):
        params = {}
        if force is not None:
            params["force"] = force
        if wait is not None:
            params["wait"] = wait

        self.post(path="stop_all", params=params)

    def kill_service(self) -> str:
        """
        WARNING: Killing the service does not kill the running workers processes.
        """
        try:
            self.post(path="kill_service")
            return "server is still up"
        except requests.exceptions.ConnectionError:
            return "server was stopped successfully"

    def start_worker(self, name: Optional[str] = None, data: Optional[dict] = None):
        params = dict(name=name) if name else None
        return self.post(path="start_worker", data=data, params=params)

    def stop_worker(self, uid: Optional[str] = None, name: Optional[str] = None):
        params = {}
        if uid is not None:
            params["uid"] = uid
        if name is not None:
            params["name"] = name
        return self.post(path=f"stop_worker", params=params)
