from .py.io.multi_lora_loader import *
from .py.io.csv_prompts_loader import *
from .py.conditioning.random_prompt import *
from .py.conditioning.combine_prompts import *
# from .malefish import init

NODE_CLASS_MAPPINGS = {
    "MultiLoraLoader": MultiLoraLoader,
    "RandomPrompt": RandomPrompt,
    "CombinePrompt": CombinePrompts,
    "CSVPromptsLoader": CSVPromptsLoader
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiLoraLoader": "Multi Lora Loader",
    "RandomPrompt": "Random (Prompt)",
    "CombinePrompt": "Combine (Prompt)",
    "CSVPromptsLoader": "CSV Prompts Loader"
}

# init()

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS",
           "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
