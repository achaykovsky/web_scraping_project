# Animal and Adjective Extractor

This Python script is designed to extract pairs of animals and their associated adjectives from Wikipedia tables. It utilizes the BeautifulSoup library for web scraping and requests for fetching HTML content from a given URL.

## Prerequisites

- Python 3.x
- `requests` library
- `BeautifulSoup` library

## Functions

### `fetch_url(url)`

Fetches the content of the given URL using the `requests` library.

### `parse_page_content(response)`

Parses the HTML content of the response using BeautifulSoup.

### `find_column_indices(header_row)`

Finds the indices of columns containing the animal names and their associated adjectives.

### `strip_non_letters(input_string)`

Strips non-letter characters from a given string using regex.

### `extract_animal_info(soup)`

Extracts animal names and their associated adjectives from Wikipedia tables.

### `clean_cell(cell_index, columns)`

Cleans the text from a specific cell of a table column.

### `log_animal_info(collateral_adjective_list, animal_name_list)`

Logs the extracted animal-adjective pairs.

### `validate_word_existence(word)`

Validates the existence of a word.

### `remove_invalid_words(words_list)`

Removes invalid words from a list based on a predefined vocabulary.

### `get_animal_names_and_adjectives(url)`

Main function to initiate the extraction process by fetching the URL, parsing the content, and extracting animal-adjective pairs.
