from typing import Optional, List

from service_sdk.exceptions import WorkerNameAlreadyUsed
from service_sdk.worker.worker import Worker


class Registry:
    def __init__(self, max_workers: int = 1):
        self._max_workers = max_workers
        self._workers_count = 0
        self._worker_by_uid = {}
        self._worker_by_name = {}

    @property
    def max(self) -> int:
        return self._max_workers

    @property
    def counter(self) -> int:
        return self._workers_count

    def add(self, worker: Worker) -> None:
        if self.get_by_name(name=worker.name):
            raise WorkerNameAlreadyUsed("Worker name is already used")
        self._worker_by_uid[worker.uid] = worker
        self._worker_by_name[worker.name] = worker
        self._workers_count += 1

    def remove(self, uid: Optional[str] = None, name: Optional[str] = None) -> None:
        if uid:
            worker_to_remove = self._worker_by_uid[uid]
        elif name:
            worker_to_remove = self._worker_by_name[name]
        else:
            return

        del self._worker_by_uid[worker_to_remove.uid]
        del self._worker_by_name[worker_to_remove.name]
        self._workers_count -= 1

    def all(self) -> List[Worker]:
        return list(self._worker_by_uid.values())

    def get_by_uid(self, uid: str) -> Optional[Worker]:
        return self._worker_by_uid.get(uid)

    def get_by_name(self, name: str) -> Optional[Worker]:
        return self._worker_by_name.get(name)
