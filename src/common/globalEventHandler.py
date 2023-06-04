import functools
from PyQt6 import QtCore


@functools.lru_cache()
class GlobalEventHandler(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._events = {}

    def addEventListener(self, name, func):
        if name not in self._events:
            self._events[name] = [func]
        else:
            self._events[name].append(func)

    def dispatchEvent(self, name):
        functions = self._events.get(name, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, func)

    def dispatchEventWithParams(self, name, *params):
        functions = self._events.get(name, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, lambda: func(*params))


GlobalEventHandlerObject = GlobalEventHandler()
