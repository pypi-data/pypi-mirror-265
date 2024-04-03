# -*- coding=utf-8 -*-
r"""

"""
import io
import typing as t
from os import PathLike
from ..structures import Caption


def write_subrip(captions: t.List[Caption], filename: t.Union[str, PathLike, t.TextIO]) -> None:
    stream = io.StringIO()

    for i, caption in enumerate(captions):
        if i != 0:
            stream.write("\r\n")

        stream.write(f"{i+1}\r\n")
        stream.write(f"{format_ts(caption.start)} --> {format_ts(caption.end)}\r\n")
        for line in caption.lines:
            stream.write(f"{line}\r\n")

    if isinstance(filename, (str, PathLike)):
        with open(filename, 'w') as file:
            file.write(stream.getvalue())
    else:
        filename.write(stream.getvalue())


def format_ts(ts: float) -> str:
    seconds = ts % 60
    minutes = int((ts / 60) % 60)
    hours = int(ts / 3600)

    return f"{hours:0>2}:{minutes:0>2}:{format(seconds, '.3f').replace('.', ','):0>6}"
