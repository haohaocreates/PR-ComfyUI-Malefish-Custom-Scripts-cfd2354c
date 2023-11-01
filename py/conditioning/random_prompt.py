from pathlib import Path

import folder_paths
import logging

from collections.abc import Iterable
from abc import ABC
from dynamicprompts.sampling_context import SamplingContext
from dynamicprompts.enums import SamplingMethod
from dynamicprompts.wildcards.wildcard_manager import WildcardManager
import re

logger = logging.getLogger(__name__)
wildcardManager = WildcardManager(
    Path(folder_paths.get_folder_paths("wildcards")[0]))


class RandomPrompt(ABC):
    def __init__(self):
        self._current_prompt = None
        self.lora_spec_re = re.compile("(<(?:lora|lyco):[^>]+>)")
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }
    
    @classmethod
    def IS_CHANGED(cls, text):
        # Force re-evaluation of the node
        return float("NaN")

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "loras",)

    FUNCTION = "process"

    # OUTPUT_NODE = False

    CATEGORY = "Malefish/conditioning"

    @property
    def context(self) -> SamplingContext:
        return SamplingContext(
            wildcard_manager=wildcardManager,
            default_sampling_method=SamplingMethod.RANDOM,
        )

    def _get_next_prompt(self, prompts: Iterable[str], current_prompt: str) -> str:
        """
        Get the next prompt from the prompts generator.
        """
        try:
            return next(prompts)
        except (StopIteration, RuntimeError):
            self._prompts = self.context.sample_prompts(current_prompt)
            try:
                return next(prompts)
            except StopIteration:
                logger.exception("No more prompts to generate!")
                return ""

    def has_prompt_changed(self, text: str) -> bool:
        """
        Check if the prompt has changed.
        """
        return self._current_prompt != text

    def process(self, text):
        if text.strip() == "":
            return ("",)

        if self.has_prompt_changed(text):
            self._current_prompt = text
            self._prompts = self.context.sample_prompts(self._current_prompt)

        if self._prompts is None:
            logger.exception("Something went wrong. Prompts is None!")
            return ("",)

        if self._current_prompt is None:
            logger.exception("Something went wrong. Current prompt is None!")
            return ("",)

        new_prompt = self._get_next_prompt(self._prompts, self._current_prompt)

        extracted_loras = self.lora_spec_re.findall(new_prompt)
        filtered_text = self.lora_spec_re.sub("", new_prompt)

        print(f"New prompt: {new_prompt}")
        return (filtered_text, "\n".join(extracted_loras),)
