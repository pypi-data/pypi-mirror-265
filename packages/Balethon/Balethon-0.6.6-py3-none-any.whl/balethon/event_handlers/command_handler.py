from inspect import getfullargspec

from .message_handler import MessageHandler
from ..conditions import text, command
from ..objects import Message


class CommandHandler(MessageHandler):
    can_handle = Message

    @staticmethod
    def get_min_arguments(callback):
        args, _, __, defaults, ___, ____, _____ = getfullargspec(callback)
        args_count = len(args)
        defaults_count = 0 if defaults is None else len(defaults)
        return args_count - defaults_count

    @staticmethod
    def get_max_arguments(callback):
        args, varargs, _, __, ___, ____, _____ = getfullargspec(callback)
        if varargs is not None:
            return None
        return len(args)

    def __init__(self, callback, condition=None, name=None, min_arguments=None, max_arguments=None):
        if name is None:
            name = callback.__name__
        if min_arguments is None:
            min_arguments = self.get_min_arguments(callback)
        if max_arguments is None:
            max_arguments = self.get_max_arguments(callback)
        command_condition = command(name, min_arguments, max_arguments)
        if condition is None:
            condition = text & command_condition
        else:
            condition = text & command_condition & condition
        super().__init__(callback, condition)

    def __call__(self, *args, client=None, event=None, **kwargs):
        if client is not None:
            kwargs["client"] = client
        if event is not None:
            kwargs["message"] = event
            _, *arguments = event.text.split()
            args += tuple(arguments)
        return super().__call__(*args, **kwargs)
