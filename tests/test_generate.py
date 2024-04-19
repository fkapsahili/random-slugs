import unittest

from randomslugs.generate import format_slug, generate_slug
from randomslugs.words import vocabulary


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
