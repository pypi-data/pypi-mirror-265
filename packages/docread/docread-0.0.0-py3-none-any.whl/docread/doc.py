import json

class Document:
    def __init__(self) -> None:
        self._doc = {
            "metadata": {},
            "pages": [],
            "gists": []
        }

        self._paragraph_map = []
        self._paragraphs = []

    def labeld_paragraphs(self, min_len=100):
        paragraphs = []
        self._paragraphs = []
        self._paragraph_map = []

        for page_num, page in enumerate(self.pages):
            for pnum, p in enumerate(page):
                label = f"⟨{len(paragraphs)}⟩"
                paragraph = p + label
                paragraphs.append(paragraph)
                self._paragraphs.append(p)
                self._paragraph_map.append((page_num, pnum))
        return paragraphs

    def dict(self):
        return self._doc

    def load(self, file):
        with open(file, "r") as f:
            self._doc = json.loads(f.read())

    def dump(self, file):
        with open(file, "w") as f:
            f.write(json.dumps(self._doc))

    def json(self, ensure_ascii=False, indent=False):
        return json.dumps(self._doc, ensure_ascii=False, indent=False)

    def get_paragraphs(self, start, end):
        if self._paragraphs is None:
            self.labeld_paragraphs()
        texts = []
        for i in range(start, end + 1):
            texts.append(self._paragraphs[i])
        return "".join(texts)

    def get_paragraph_index(self, label):
        if self._paragraph_map is None:
            self.labeld_paragraphs()
        return self._paragraph_map[label]

    @property
    def metadata(self):
        return self._doc["metadata"]

    @metadata.setter
    def metadata(self, metadata):
        self._doc["metadata"] = metadata

    @property
    def pages(self, paragraph_label=False):
        return self._doc["pages"]

    @pages.setter
    def pages(self, pages):
        self._doc["pages"] = pages

    @property
    def paragraphs(self):
        return self._doc["paragraphs"]

    @paragraphs.setter
    def paragraphs(self, paragraphs):
        self._doc["paragraphs"] = paragraphs

    @property
    def gists(self):
        return self._doc["gists"]

    @gists.setter
    def gists(self, gists):
        self._doc["gists"] = gists

    @property
    def progress(self):
        return self._doc.get("progress")

    @progress.setter
    def progress(self, progress):
        self._doc["progress"] = progress
