from enum import Enum, auto


class CmdExt(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Cmd(CmdExt):
    SETUP = auto()
    RUN = auto()
    ALL = auto()
