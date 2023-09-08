import gzip
import json
import os
from typing import Dict, Iterable, List


def load_jsonl_into(input_file_name: str, data: List) -> None:
    with open(input_file_name, "r") as json_file:
        # prefer readable json
        content = ""
        for line in json_file:
            content += line.strip()
            if line.startswith("}"):  # end of a JSON object
                data.append(json.loads(content))
                content = ""


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False, indent=4):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = "ab"
    else:
        mode = "wb"
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode="wb") as gzfp:
                for x in data:
                    if indent == 0:
                        gzfp.write((json.dumps(x) + "\n").encode("utf-8"))
                    else:
                        gzfp.write((json.dumps(x, indent=indent) + "\n").encode("utf-8"))
    else:
        with open(filename, mode) as fp:
            for x in data:
                if indent == 0:
                    fp.write((json.dumps(x) + "\n").encode("utf-8"))
                else:
                    fp.write((json.dumps(x, indent=indent) + "\n").encode("utf-8"))
