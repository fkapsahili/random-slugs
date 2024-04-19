import logging
import random
from typing import Dict, List, Literal, TypedDict

from randomslugs.words import get_words_by_category

logger = logging.getLogger(__name__)

FORMAT_OPTION = Literal["kebab", "snake", "camel"]

DEFAULT_NUMBER_OF_WORDS = 3
DEFAULT_FORMAT_OPTION = "kebab"

Options = TypedDict(
    "Options",
    {"parts_of_speech": List[str], "categories": Dict, "format": FORMAT_OPTION, "seed": None},
)


def generate_slug(num_of_words=DEFAULT_NUMBER_OF_WORDS, options: Options = None) -> str:
    words = []
    opts = _get_default_options(num_of_words)

    if options is not None:
        opts.update(options)

    if isinstance(opts["seed"], (int, str, float, bytes, bytearray)):
        random.seed(opts["seed"])

    for part in opts["parts_of_speech"]:
        if part in opts["categories"]:
            categories = opts["categories"][part]
        else:
            categories = []
        candidates = get_words_by_category(part, categories=categories)
        candidate = random.choice(candidates)
        words.append(candidate)

    return format_slug(words, opts["format"])


def _get_default_options(num_of_words=DEFAULT_NUMBER_OF_WORDS):
    parts_of_speech = []
    for _i in range(num_of_words - 1):
        parts_of_speech.append("adjectives")
    parts_of_speech.append("nouns")

    default_options = {
        "parts_of_speech": parts_of_speech,
        "categories": {},
        "format": DEFAULT_FORMAT_OPTION,
        "seed": None,
    }
    return default_options


def format_slug(words: List[str], fmt: FORMAT_OPTION = DEFAULT_FORMAT_OPTION) -> str:
    if fmt == "kebab":
        return "-".join(words)
    elif fmt == "snake":
        return "_".join(words)
    elif fmt == "camel":
        return "".join([words[0]] + [word.capitalize() for word in words[1:]])
