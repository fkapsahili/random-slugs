import logging
import random
from typing import List, Literal, TypedDict

from random_slugs.words import get_words_by_category

logger = logging.getLogger(__name__)

FORMAT_OPTION = Literal["kebab", "snake", "camel"]

DEFAULT_NUMBER_OF_WORDS = 3
DEFAULT_FORMAT_OPTION = "kebab"

Options = TypedDict(
    "Options",
    {"parts_of_speech": List[str], "categories": dict, "format": FORMAT_OPTION, "seed": None},
)


class RandomSlugsError(Exception):
    """
    Custom exception for all errors related to slug generation.
    """

    pass


class RandomSlugConfigError(RandomSlugsError):
    """
    Exception for all configuration errors related.
    """

    pass


def generate_slug(num_of_words: int = DEFAULT_NUMBER_OF_WORDS, options: Options = None) -> str:
    """
    Generates a random slug based on the given options.
    """
    words = []
    opts = _get_default_options(num_of_words)

    if options is not None:
        _validate_options(options)
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


def _get_default_parts_of_speech(num_of_words: int) -> List[str]:
    parts_of_speech = []
    for _ in range(num_of_words - 1):
        parts_of_speech.append("adjectives")
    parts_of_speech.append("nouns")
    return parts_of_speech


def _get_default_options(num_of_words: int = DEFAULT_NUMBER_OF_WORDS) -> Options:
    default_options = {
        "parts_of_speech": _get_default_parts_of_speech(num_of_words),
        "categories": {},
        "format": DEFAULT_FORMAT_OPTION,
        "seed": None,
    }
    return default_options


def _validate_options(options: Options) -> None:
    if "parts_of_speech" in options:
        for part in options["parts_of_speech"]:
            if part not in ["adjectives", "nouns"]:
                raise RandomSlugConfigError(f"Invalid part of speech: {part}")
    if "categories" in options:
        for part, _categories in options["categories"].items():
            if part not in ["adjectives", "nouns"]:
                raise RandomSlugConfigError(f"Invalid part of speech: {part}")
    if "format" in options:
        if options["format"] not in ["kebab", "snake", "camel"]:
            raise RandomSlugConfigError(f"Invalid format: {options['format']}")
    if "seed" in options:
        if not isinstance(options["seed"], (int, str, float, bytes, bytearray)):
            raise RandomSlugConfigError(f"Invalid seed: {options['seed']}")


def format_slug(words: List[str], fmt: FORMAT_OPTION = DEFAULT_FORMAT_OPTION) -> str:
    """
    Formats a list of words into a slug based on the given format.
    """
    if fmt == "kebab":
        return "-".join(words)
    elif fmt == "snake":
        return "_".join(words)
    elif fmt == "camel":
        return "".join([words[0]] + [word.capitalize() for word in words[1:]])


def get_total_unique_slugs(
    number_of_words: int = DEFAULT_NUMBER_OF_WORDS, options: Options = None
) -> int:
    """
    Returns the total number of unique slugs that can be generated with the given options.
    """
    if options is None:
        options = _get_default_options(number_of_words)

    num_adjectives = len(
        get_words_by_category("adjectives", options.get("categories", {}).get("adjectives", []))
    )
    num_nouns = len(get_words_by_category("nouns", options.get("categories", {}).get("nouns", [])))
    nums = {"adjectives": num_adjectives, "nouns": num_nouns}

    num_words = number_of_words or DEFAULT_NUMBER_OF_WORDS
    parts_of_speech = options.get("parts_of_speech", _get_default_parts_of_speech(num_words))

    combos = 1
    for i in range(num_words):
        combos *= nums[parts_of_speech[i]]

    return combos
