from pathlib import Path

import folder_paths
import logging

from collections.abc import Iterable
from abc import ABC
from dynamicprompts.sampling_context import SamplingContext
from dynamicprompts.enums import SamplingMethod
from dynamicprompts.generators import RandomPromptGenerator
from dynamicprompts.wildcards.wildcard_manager import WildcardManager
import re

logger = logging.getLogger(__name__)
wildcardManager = WildcardManager(
    Path(folder_paths.get_folder_paths("wildcards")[0]))


class CombinePrompts(ABC):
    def __init__(self):
        self._current_full_prompt = None
        self._current_face_prompt = None
        self.lora_spec_re = re.compile("(<(?:lora|lyco):[^>]+>)")
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "styles": ("STRING", {
                    "multiline": True,
                    "default": "masterpiece"
                }),
                "face": ("STRING", {
                    "multiline": True,
                    "default": "1girl"
                }),
                "cloth": ("STRING", {
                    "multiline": True,
                    "default": "dress"
                }),
                "action": ("STRING", {
                    "multiline": True,
                    "default": "standing"
                }),
                "face_action": ("STRING", {
                    "multiline": True,
                    "default": "smile"
                }),
                "environment": ("STRING", {
                    "multiline": True,
                    "default": "forest"
                }),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            },
            "optional": {
                "added_styles": ("STRING", {"forceInput": True}),
                "added_face": ("STRING", {"forceInput": True}),
                "added_cloth": ("STRING", {"forceInput": True}),
                "added_action": ("STRING", {"forceInput": True}),
                "added_face_action": ("STRING", {"forceInput": True}),
                "added_environment": ("STRING", {"forceInput": True}),
            }
        }

    @classmethod
    def IS_CHANGED(cls, text):
        # Force re-evaluation of the node
        return float("NaN")

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("full", "face_only", "full_loras", "face_loras")

    FUNCTION = "process"

    # OUTPUT_NODE = False

    CATEGORY = "Malefish/conditioning"

    @property
    def generator(self) -> RandomPromptGenerator:
        return RandomPromptGenerator(
            wildcard_manager=wildcardManager,
        )

    def process(self,
                styles, face, cloth, action, face_action, environment, seed,
                added_styles="", added_face="", added_cloth="", added_action="", added_face_action="", added_environment=""
                ):
        full = ""
        faceOnly = ""

        if styles != "":
            full += styles
            faceOnly += styles

        if added_styles != "":
            full += ", \n" + added_styles
            faceOnly += ", \n" + added_styles

        if face != "":
            full += ", \n" + face
            faceOnly += ", \n" + face

        if added_face != "":
            full += ", \n" + added_face
            faceOnly += ", \n" + added_face

        if cloth != "":
            full += ", \n" + cloth

        if added_cloth != "":
            full += ", \n" + added_cloth

        if action != "":
            full += ", \n" + action

        if added_action != "":
            full += ", \n" + added_action

        if face_action != "":
            full += ", \n" + face_action
            faceOnly += ", \n" + face_action

        if added_face_action != "":
            full += ", \n" + added_face_action
            faceOnly += ", \n" + added_face_action

        if environment != "":
            full += ", \n" + environment

        if added_environment != "":
            full += ", \n" + added_environment

        if full.strip() == "" and faceOnly.strip() == "":
            return ("",)\


        full = self.generator.generate(full, num_images=1, seeds=seed)[0]
        faceOnly = self.generator.generate(
            faceOnly, num_images=1, seeds=seed)[0]

        fullExtractedLoras = self.lora_spec_re.findall(full)
        fullFilteredText = self.lora_spec_re.sub("", full)

        faceExtractedLoras = self.lora_spec_re.findall(faceOnly)
        faceFilteredText = self.lora_spec_re.sub("", faceOnly)

        return (fullFilteredText, faceFilteredText, "\n".join(fullExtractedLoras), "\n".join(faceExtractedLoras))
