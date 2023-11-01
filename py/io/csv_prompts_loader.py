import logging
import os
import pathlib
import pandas as pd

logger = logging.getLogger(__name__)


class CSVPromptsLoader():
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "remove_extension": ([
                    "On",
                    "Off"],)
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("styles", "face", "cloth", "action", "face_action",)

    FUNCTION = "process"

    # OUTPUT_NODE = False

    CATEGORY = "Malefish/io"

    @classmethod
    def IS_CHANGED(cls, text):
        # Force re-evaluation of the node
        return float("NaN")

    def process(self, path, key, remove_extension):
        if path.strip() == "":
            return ("", "", "", "", "",)

        if not os.path.exists(path):
            logger.exception("Path is not exist")
            return ("", "", "", "", "",)

        file_extension = pathlib.Path(path).suffix

        if file_extension != ".csv":
            logger.exception("file is not csv")
            return ("", "", "", "", "",)

        df = pd.read_csv(path, index_col=0, dtype={
                         "name": 'string', "styles": 'string', "face": 'string', "cloth": 'string', "action": 'string', "face_action": 'string'})

        if remove_extension == "On":
            key = os.path.splitext(key)[0]

        try:
            values = df.loc[key]
        except KeyError:
            logger.exception("Key is not exist")
            return ("", "", "", "", "",)

        return (values['styles'], values['face'], values['cloth'], values['action'], values['face_action'],)
