# Random Slugs

`random-slugs` is a user-friendly Python package that generates those random word slugs. This package is customizable and allows users to specify the parts of speech, categories of words, and the reproducibility.

## Features
- Generate slugs with a specified number of words
- Customize the parts of speech and categories of words used
- Choose the format of the slug (`kebab-case`, `snake_case` or `camelCase`)
- Set a random seed for reproducibility
- Handle errors gracefully with custom exceptions

## Installation
You can install `random-slugs` using pip:

```bash
pip install random-slugs
```

## Usage
Here is a basic example of how to use the package:
```python
from random_slugs import generate_slug

slug = generate_slug()
print(slug) # E.g. 'quick-brown-fox'
```

### Customize the Slug
You can customize the slug generation by passing an `options` dictionary to the `generate_slug` function:
```python
options = {
    "parts_of_speech": ["adjectives", "nouns"],
    "categories": {"adjectives": ["color"], "nouns": ["animal"]},
    "format": "snake",
    "seed": 42
}

slug = generate_slug(num_of_words=2, options=options)
print(slug)  # E.g. : 'brown_fox'
```

## API
`generate_slug`
```python
generate_slug(num_of_words: int = 3, options: Options = None) -> str
```
Generates a random slug.

**Parameters**:
- `num_of_words` (int): The number of words to include in the slug. Defaults to 3.
- `options` (Options): A dictionary of options to customize the slug generation.

**Options**:
- `parts_of_speech` (List[str]): List of parts of speech to use. Must be one of: `adjectives`, `nouns`.
- `categories` (Dict): A dictionary mapping parts of speech to categories of words. E.g. `{"adjectives": ["color"], "nouns": ["animal"]}`.
    - **Adjective Categories:**
        - `color`
        - `condition`
        - `emotion`
        - `size`
        - `quantity`
    - **Noun Categories:**
        - `animal`
        - `color`
        - `pokemon`
        - `profession`
        - `technology`
        - `thing`
        - `transport`

- `format` (str): The format of the slug. Must be one of: `kebab`, `snake`, `camel`. Defaults to `kebab`.
- `seed` (int): The random seed value to use for reproducibility.

**Returns**:
- `str`: The generated slug.

### Total Unique Slugs
The total number of unique slugs that can be generated is calculated as follows:
```python
from random_slugs import get_total_unique_slugs

total = get_total_unique_slugs()
print(total)  # 6254859
```

### Exceptions
- `RandomSlugsError`: Base class for all exceptions in the package.
- `RandomSlugConfigError`: Exception for configuration errors.

## Example
Here is a complete example that includes custom options and error handling:
```python
from random_slugs import generate_slug, RandomSlugConfigError

options = {
    "parts_of_speech": ["adjectives", "nouns"],
    "categories": {"adjectives": ["size"], "nouns": ["animal"]},
    "format": "camel",
    "seed": "example_seed"
}

try:
    slug = generate_slug(num_of_words=2, options=options)
    print(slug)  # E.g. "bigCat"
except RandomSlugConfigError as e:
    print(f"Configuration error: {e}")
except RandomSlugsError as e:
    print(f"Slug generation error: {e}")
```

# Testing
You can run the test suite using the following command:
```bash
pytest tests
```

# Contributing
Contributions are welcome! Please open an issue or submit a pull request.

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.