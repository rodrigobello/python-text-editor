from copy import deepcopy


class History:
    def __init__(self, snapshots=None):
        self._snapshots = snapshots or []

    def save_snapshot(self, buffer, cursor):
        snapshot = (deepcopy(buffer), deepcopy(cursor))
        self._snapshots.append(snapshot)

    def restore_snapshot(self):
        if self._snapshots:
            return self._snapshots.pop()
        raise self.EmptyHistoryException()

    class EmptyHistoryException(Exception):
        pass
