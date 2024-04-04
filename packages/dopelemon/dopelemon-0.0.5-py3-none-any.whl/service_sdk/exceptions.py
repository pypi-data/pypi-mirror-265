class StopGracefullyException(Exception):
    pass


class TimeoutWaitingForWorkerToStop(Exception):
    pass


class WorkerNameAlreadyUsed(ValueError):
    pass


class CannotExceedMaxWorkersLimit(RuntimeError):
    pass
