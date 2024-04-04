from multiprocessing import Process
from time import sleep
from typing import Callable, Any, Optional

from service_sdk.exceptions import StopGracefullyException
from service_sdk.manager.controller import Controller
from service_sdk.utils import generate_id, setup_logger
from service_sdk.worker.ex_thread import ExThread


class Worker:
    def __init__(
            self,
            controller: Controller,
            work_callback: Callable[[Any], Any],
            name: Optional[str] = None,
            uid: Optional[str] = None,
            data: Optional[dict] = None,
            **kwargs
    ):
        self.work_callback = work_callback
        self.controller = controller
        self.uid = uid or generate_id()
        self.name = name or self.uid
        self.data = data or {}
        self.process = Process(target=self.handle_work, kwargs=kwargs)
        self.context = dict(uid=self.uid, name=self.name, data=self.data)

    def get_pid(self) -> Optional[int]:
        return self.process.pid

    def start(self):
        self.process.start()

    def handle_work(self, **kwargs):
        logger = setup_logger()
        counter = 0
        logger.info("Starting work")

        working_thread = ExThread(target=self.work_callback, daemon=True, kwargs=dict(context=self.context))
        working_thread.start()
        try:
            while not self.controller.get_stop():
                counter += 1
                self.controller.set_status(counter)
                sleep(1)

            logger.info("Stop command received. Shutting worker down.")
            working_thread.raise_exception(exception=StopGracefullyException)
        except KeyboardInterrupt as exception:
            logger.info(f"{exception.__class__.__name__} received. Shutting worker down.")
