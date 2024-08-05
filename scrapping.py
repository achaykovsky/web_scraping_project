import logging
import re
from typing import List

import requests
from bs4 import BeautifulSoup

ANIMAL_COL_NAME = "animal"
COLLATERAL_ADJECTIVE_COL_NAME = "collateral adjective"

INVALID_WORDS_VOC = (
    "or",
    "for",
    "on",
    "a",
    "of",
    "list",
    "male",
    "female",
    "young",
    "also",
    "see",
)


def fetch_url(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as request_error:
        logger.error(f"Request error: {request_error}")
        return None


def parse_page_content(response):
    if response and response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    return None


def find_column_indices(header_row):
    collective_noun_index = None
    collateral_adjective_index = None
    if header_row:
        columns = header_row.find_all(["td", "th"])

        if len(columns) == 0:
            logger.warning("Row does not have enough columns. Skipping.")

        for index, column in enumerate(columns):
            column_text = column.get_text(strip=True).lower()

            if ANIMAL_COL_NAME in column_text:
                collective_noun_index = index
            elif COLLATERAL_ADJECTIVE_COL_NAME in column_text:
                collateral_adjective_index = index

        return collective_noun_index, collateral_adjective_index
    return None, None


def strip_non_letters(input_string):
    # Use a regex to remove anything that is not a letter
    stripped_string = re.sub(r"[^a-zA-Z]", ",", input_string).replace(" ", "").rstrip()
    return stripped_string


def extract_animal_info(soup):
    try:
        if soup:
            tables = soup.find_all("table", {"class": "wikitable"})

            for table in tables:
                rows = table.find_all("tr")

                animal_index, collateral_adjective_index = find_column_indices(rows[0])

                if animal_index is None or collateral_adjective_index is None:
                    continue

                for row in rows[1:]:
                    columns = row.find_all(["td", "th"])

                    if len(columns) >= 2:
                        # there are rows that are grouped and are not relevant for the task,
                        # it's a validation that we have at least 2 columns
                        animals_list = clean_cell(animal_index, columns)

                        collateral_adjective_list = clean_cell(
                            collateral_adjective_index, columns
                        )

                        log_animal_info(collateral_adjective_list, animals_list)
                    else:
                        logger.warning("Row does not have enough columns. Skipping.")
    except Exception as e:
        logger.error(f"An error occurred while extracting animal info: {e}")


def clean_cell(cell_index, columns):
    text_from_object_column = columns[cell_index].get_text(strip=True)
    object_name = strip_non_letters(text_from_object_column).split(",")
    object_list = filter_invalid_words(object_name)
    return object_list


# list all the possible permutations for adjectives and animals
def log_animal_info(collateral_adjective_list, animal_name_list):
    for adjective in collateral_adjective_list:
        for animal in animal_name_list:
            if validate_word_existence(animal) and validate_word_existence(adjective):
                logger.info(f"Collateral Adjective: {adjective}, Animal: {animal}")


def validate_word_existence(word):
    if word == "" or word is None:
        return False
    return True


def filter_invalid_words(words_list: List) -> List:
    return [
        word
        for word in words_list
        if word.lower() not in INVALID_WORDS_VOC and validate_word_existence(word)
    ]


def get_animal_names_and_adjectives(url):
    response = fetch_url(url)
    soup = parse_page_content(response)
    extract_animal_info(soup)


logger = logging.getLogger(__name__)
