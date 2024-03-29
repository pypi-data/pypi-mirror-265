import json
import os
import sys
from pprint import pprint

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
#from readability import Document as ReadablityDocument
from .doc import Document


def get_metadata_value(book, name):
    m = book.get_metadata("DC", name)
    if m:
        return m[0][0]


def get_identifiers(book):
    ids = {}
    identifiers = book.get_metadata("DC", "identifier")
    for i in identifiers:
        v = list(i[1].items())
        if len(v) > 0:
            ids[v[0][1]] = i[0]
    return ids


def get_metadata(book):
    metadata = {
        "title": get_metadata_value(book, "title"),
        "creator": get_metadata_value(book, "creator"),
        "date": get_metadata_value(book, "date"),
        "identifiers": get_identifiers(book=book),
        "description": get_metadata_value(book, "description"),
        "publisher": get_metadata_value(book, "publisher"),
        "language": get_metadata_value(book, "language"),
    }

    return metadata


def extract_pages(book: epub.EpubBook):
    pages = []

    for i in book.get_items():
        if i.get_type() == ebooklib.ITEM_DOCUMENT:
            html = i.get_body_content()
            #html = ReadablityDocument(html).summary()

            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator="\n", strip=True)

            if len(text) > 0:
                paragraphs = text.split("\n")
                pages.append(paragraphs)
    return pages


def extract(path):
    book = epub.read_epub(path, options={"ignore_ncx": True})
    metadata = get_metadata(book)
    pages = extract_pages(book)

    doc = Document()
    doc.metadata = metadata
    doc.pages = pages

    return doc


def extract_file(src, dst):
    def _extract_file(src, dst):
        doc = extract(src)
        json_data = doc.json()

        with open(dst, "w") as f:
            f.write(json_data)

    if os.path.isdir(src):
        if not os.path.isdir(dst):
            print(f"dst must be a dir")
            sys.exit(-1)

        for fname in os.listdir(src):
            dst_fname = fname[:-5] + ".json"
            dst_path = os.path.join(dst, dst_fname)

            if not fname.endswith(".epub") or os.path.exists(dst_path):
                print(f"skip: {fname}")
                continue

            print(f"extracting: {fname}")

            extract_file(os.path.join(src, fname), dst_path)
    else:
        extract_file(src, dst)
