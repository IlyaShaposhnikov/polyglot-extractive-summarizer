#!/usr/bin/env python3
import logging
import nltk

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

REQUIRED_PACKAGES = ['punkt', 'punkt_tab', 'stopwords']


def download_nltk_packages(packages: list[str]) -> bool:
    """Download specified NLTK packages. Return True if all succeed."""
    all_ok = True
    for pkg in packages:
        try:
            if nltk.download(pkg, quiet=True):
                logging.info("Package '%s' is ready.", pkg)
            else:
                logging.error("Failed to download package '%s'.", pkg)
                all_ok = False
        except Exception as e:
            logging.error("Error downloading '%s': %s", pkg, e)
            all_ok = False
    return all_ok


if __name__ == "__main__":
    if download_nltk_packages(REQUIRED_PACKAGES):
        logging.info("All NLTK components installed successfully.")
    else:
        logging.error("Some NLTK components could not be installed.")
