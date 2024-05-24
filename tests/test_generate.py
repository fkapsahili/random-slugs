import unittest

from random_slugs.generate import (
    RandomSlugConfigError,
    format_slug,
    generate_slug,
    get_total_unique_slugs,
)
from random_slugs.words import vocabulary


def check_word_in_category(part_of_speech, word, categories) -> bool:
    cats = set(categories)
    for vocab in vocabulary[part_of_speech]:
        if vocab[0] == word:
            return len(cats.intersection(vocab[1])) > 0
    return False


class RandomSlugsTest(unittest.TestCase):
    def test_generate_slug(self):
        slug = generate_slug()
        self.assertIsInstance(slug, str)
        self.assertTrue(len(slug) > 10)

    def test_parts_are_unique(self):
        slug = generate_slug()
        words = slug.split("-")
        self.assertEqual(len(words), len(set(words)))

    def test_number_of_words(self):
        sizes = [2, 3, 4, 5, 6]
        for size in sizes:
            slug = generate_slug(size)
            words = slug.split("-")
            self.assertEqual(len(words), size)

    def test_words_in_specified_category(self):
        options = {
            "categories": {
                "nouns": ["pokemon"],
                "adjectives": ["color"],
            }
        }
        slug = generate_slug(3, options)
        chunks = slug.split("-")
        self.assertTrue(
            check_word_in_category("adjectives", chunks[0], options["categories"]["adjectives"])
        )
        self.assertTrue(
            check_word_in_category("adjectives", chunks[1], options["categories"]["adjectives"])
        )
        self.assertTrue(check_word_in_category("nouns", chunks[2], options["categories"]["nouns"]))

    def test_if_random_seed_is_set_slug_should_be_equal(self):
        options = {"seed": 42}
        slug1 = generate_slug(options=options)
        slug2 = generate_slug(options=options)
        slug3 = generate_slug(options={"seed": 43})
        self.assertEqual(slug1, slug2)
        self.assertNotEqual(slug1, slug3)

    def test_if_random_seed_is_set_slug_should_be_different(self):
        slug1 = generate_slug()
        slug2 = generate_slug()
        self.assertNotEqual(slug1, slug2)

    def test_invalid_options_seed(self):
        with self.assertRaises(RandomSlugConfigError):
            generate_slug(options={"seed": None})

    def test_invalid_options_parts_of_speech(self):
        with self.assertRaises(RandomSlugConfigError):
            generate_slug(options={"parts_of_speech": ["invalid"]})

    def test_invalid_options_categories(self):
        with self.assertRaises(RandomSlugConfigError):
            generate_slug(options={"categories": {"invalid": []}})

    def test_invalid_options_format(self):
        with self.assertRaises(RandomSlugConfigError):
            generate_slug(options={"format": "invalid"})

    def test_invalid_options_seed_type(self):
        with self.assertRaises(RandomSlugConfigError):
            generate_slug(options={"seed": {}})

    def test_empty_options_parts_of_speech_type(self):
        generate_slug(options={"parts_of_speech": {}})


class FormatSlugTest(unittest.TestCase):
    def test_kebab_case(self):
        words = ["red", "panda"]
        slug = format_slug(words, "kebab")
        self.assertEqual(slug, "red-panda")

    def test_snake_case(self):
        words = ["red", "panda"]
        slug = format_slug(words, "snake")
        self.assertEqual(slug, "red_panda")

    def test_camel_case(self):
        words = ["red", "panda"]
        slug = format_slug(words, "camel")
        self.assertEqual(slug, "redPanda")

    def test_default_format(self):
        words = ["red", "panda"]
        slug = format_slug(words)
        self.assertEqual(slug, "red-panda")


class TotalUniqueSlugsTest(unittest.TestCase):
    def setUp(self):
        self.all_adjectives = [v[0] for v in vocabulary["adjectives"]]
        self.all_nouns = [v[0] for v in vocabulary["nouns"]]
        self.num_adjectives = len(self.all_adjectives)
        self.num_nouns = len(self.all_nouns)

    def test_total_unique_slugs(self):
        num = get_total_unique_slugs()
        total = self.num_adjectives * self.num_adjectives * self.num_nouns
        self.assertEqual(num, total)

    def test_total_in_subsets_of_categories(self):
        options = {
            "categories": {
                "nouns": ["animal", "technology"],
                "adjectives": ["color", "size"],
            }
        }
        num = get_total_unique_slugs(4, options)
        num_adjectives = len(
            [
                word
                for word, categories in vocabulary["adjectives"]
                if any(category in categories for category in options["categories"]["adjectives"])
            ]
        )
        num_nouns = len(
            [
                word
                for word, categories in vocabulary["nouns"]
                if any(category in categories for category in options["categories"]["nouns"])
            ]
        )
        total = num_adjectives**3 * num_nouns
        self.assertEqual(num, total)
