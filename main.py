import logging

from scrapping import get_animal_names_and_adjectives, logger

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    wikipedia_url = "https://en.wikipedia.org/wiki/List_of_animal_names"

    try:
        get_animal_names_and_adjectives(wikipedia_url)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
