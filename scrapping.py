import logging
import re
from typing import List

import requests
from bs4 import BeautifulSoup

COLLECTIVE_NOUN = 'collective noun'
COLLATERAL_ADJECTIVE = 'collateral adjective'


def fetch_url(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as request_error:
        logger.error(f"Request error: {request_error}")
        return None


def parse_page_content(response):
    if response and response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    return None


def find_column_indices(header_row):
    collective_noun_index = None
    collateral_adjective_index = None
    if header_row:
        columns = header_row.find_all(['td', 'th'])

        if len(columns) == 0:
            logger.warning("Row does not have enough columns. Skipping.")

        for index, column in enumerate(columns):
            column_text = column.get_text(strip=True).lower()

            if COLLECTIVE_NOUN in column_text:
                collective_noun_index = index
            elif COLLATERAL_ADJECTIVE in column_text:
                collateral_adjective_index = index

        return collective_noun_index, collateral_adjective_index
    return None, None


def strip_non_letters(input_string):
    # Use a regex to remove anything that is not a letter
    stripped_string = re.sub(r'[^a-zA-Z]', ',', input_string).replace(' ', '').rstrip()
    return stripped_string


def extract_animal_info(soup):
    try:
        if soup:
            tables = soup.find_all('table', {'class': 'wikitable'})

            for table in tables:
                rows = table.find_all('tr')

                collective_noun_index, collateral_adjective_index = find_column_indices(rows[0])

                for row in rows[1:]:
                    columns = row.find_all(['td', 'th'])

                    if len(columns) >= 2:
                        # there are rows that are grouped and are not relevant for the task,
                        # it's a validation that we have at least 2 columns
                        text_from_animal_column = columns[collective_noun_index].get_text(strip=True)
                        animals_name = strip_non_letters(text_from_animal_column).split(',')
                        animals_list = remove_invalid_words(animals_name)

                        text_from_adjective_column = columns[collateral_adjective_index].get_text(strip=True)
                        collateral_adjectives = strip_non_letters(text_from_adjective_column).split(',')
                        collateral_adjective_list = remove_invalid_words(collateral_adjectives)

                        log_animal_info(collateral_adjective_list, animals_list)
                    else:
                        logger.warning("Row does not have enough columns. Skipping.")
    except Exception as e:
        logger.error(f"An error occurred while extracting animal info: {e}")


# list all the possible permutations for adjectives and animals
def log_animal_info(collateral_adjective_list, animal_name_list):
    for adjective in collateral_adjective_list:
        for animal in animal_name_list:
            if validate_word_existence(animal) and validate_word_existence(adjective):
                logger.info(f"Collateral Adjective: {adjective}, Animal: {animal}")


def validate_word_existence(word):
    if word == '' or word is None:
        return False
    return True


def remove_invalid_words(words_list: List) -> List:
    invalid_words = ('or', 'for', 'on', 'a', 'of')
    for word in words_list:
        if word in invalid_words:
            words_list.remove(word)
    return words_list


def get_animal_names_and_adjectives(url):
    response = fetch_url(url)
    soup = parse_page_content(response)
    extract_animal_info(soup)


logger = logging.getLogger(__name__)
