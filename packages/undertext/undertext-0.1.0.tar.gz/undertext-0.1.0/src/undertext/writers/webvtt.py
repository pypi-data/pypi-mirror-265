# -*- coding=utf-8 -*-
r"""

"""
import io
import typing as t
from os import PathLike
from ..structures import Caption


def write_webvtt(captions: t.List[Caption], filename: t.Union[str, PathLike, t.TextIO],
                 header: str = None) -> None:
    stream = io.StringIO()

    stream.write("WEBVTT")
    if header is not None:
        stream.write(f" - {header}")
    stream.write("\r\n")

    for caption in captions:
        stream.write("\r\n")
        if caption.id:
            stream.write(f"{caption.id}\r\n")
        stream.write(f"{format_ts(caption.start)} --> {format_ts(caption.end)}")
        if caption.styles:
            stream.write(" ")
            for key, value in caption.styles.items():
                if key in {"line", "position", "size", "align"}:
                    stream.write(f"{key}:{value}")  # todo: cleanup of style values
                # else:  # don't raise. maybe "bad" style comes from other format
                #     raise KeyError(f"Unknown style: {key!r}")
        stream.write("\r\n")
        if len(caption.lines) == 1:
            stream.write(f"{caption.text}\r\n")
        else:
            for line in caption.lines:
                stream.write(f"- {line}\r\n")

    if isinstance(filename, (str, PathLike)):
        with open(filename, 'w') as file:
            file.write(stream.getvalue())
    else:
        filename.write(stream.getvalue())


def format_ts(ts: float) -> str:
    seconds = ts % 60
    minutes = int((ts / 60) % 60)
    hours = int(ts / 3600)

    return f"{hours:0>2}:{minutes:0>2}:{format(seconds, '.3f'):0>6}"
