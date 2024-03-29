
import re

import tiktoken
from iauto.llms import ChatMessage, Session, create_llm
from sentence_transformers import SentenceTransformer
from .doc import Document

EPISODE_PROMPT = """You are given a passage that is taken from a larger text (article, book, ...) and some numbered labels between the paragraphs in the passage.
Numbered labels are in angle brackets. For example, if the label number is 19, it shows as ⟨19⟩ in text.
Please choose a label where it is natural to break reading.
The label can be a scene transition, the end of a dialogue, the end of an argument, a narrative transition, etc.
Please answer with the break point label and explain. For example, if ⟨57⟩ is a good point to break, answer with
“Break point: ⟨57⟩\n Because ...”

Passage:
{passage}
"""

GIST_PROMPT = """Please shorten the following passage.
Just give me a shortened version. DO NOT explain your reason. DO NOT include notations.
Output language: {lang}

Passage:
{passage}
"""


class Reader:
    def __init__(
        self,
        token_limit=1000,
        text_threshold=100,
        llm_provider="openai",
        llm_args={}
    ) -> None:
        self._token_limit = token_limit
        self._text_threshold = text_threshold

        llm = create_llm(
            provider=llm_provider,
            **llm_args
        )

        self._llm_session = Session(llm=llm)

    def read(self, file, output=None, progress=True):
        if output is None:
            output = file

        doc = Document()
        doc.load(file)
        doc.metadata["token_limit"] = self._token_limit
        doc.metadata["text_threshold"] = self._text_threshold
        doc.metadata["model"] = self._llm_session.llm.model

        paragraphs = doc.labeld_paragraphs()

        token_len = 0
        win = []
        last_label = doc.metadata.get("read_progress") or -1

        token_enc = tiktoken.encoding_for_model('gpt-3.5-turbo')

        while last_label < len(paragraphs) - 1:
            idx = last_label + len(win) + 1

            the_end = False
            if idx < len(paragraphs):
                p = paragraphs[idx]
                win.append(p)

                tokens = token_enc.encode(p)
                token_len += len(tokens)
            else:
                the_end = True

            if token_len >= self._token_limit or the_end:
                text = "".join(win)
                win = []
                token_len = 0

                labels = self._extract_episodes(text)

                labels_0 = []
                for label in labels:
                    if label > last_label:
                        labels_0.append(label)
                labels = labels_0

                if len(labels) == 0:
                    labels = [idx]

                for label in labels:
                    start = last_label + 1
                    text = doc.get_paragraphs(start, label)

                    if len(text) >= self._text_threshold:
                        lang = doc.metadata.get("language") or "en"
                        gist = self._generate_gist(text, lang)

                        doc.gists.append({
                            "start": doc.get_paragraph_index(start),
                            "end": doc.get_paragraph_index(label),
                            "gist": gist,
                            "length": len(text),
                            "tokens": len(token_enc.encode(text))
                        })

                    last_label = label

                doc.metadata["read_progress"] = last_label

                doc.dump(output)

                if progress:
                    total = len(paragraphs)
                    print(f"Progress: {last_label}/{total}")

    def embed(self, file, output=None, model="BAAI/bge-reranker-base", model_cache_folder=None, model_args={}):
        if output is None:
            output = file

        doc = Document()
        doc.load(file)
        doc.metadata["embed_model"] = model

        sentences = []
        for gist in doc.gists:
            sentences.append(gist["gist"])

        model = SentenceTransformer(model, cache_folder=model_cache_folder, **model_args)
        embeds = model.encode(sentences, convert_to_numpy=True)

        for i, e in enumerate(embeds):
            doc.gists[i]["embeds"] = e.tolist()

        doc.dump(output)

    def _extract_episodes(self, text):
        prompt = EPISODE_PROMPT.format(passage=text)
        m = self._llm_session.run(
            messages=[ChatMessage(role="system", content=prompt)])
        labels = re.findall(r'⟨(\d+)⟩', m.content, re.MULTILINE | re.DOTALL)
        labels = [int(x) for x in set(labels)]
        labels.sort()
        return labels

    def _generate_gist(self, text, lang="en"):
        prompt = GIST_PROMPT.format(passage=text, lang=lang)
        m = self._llm_session.run(
            messages=[ChatMessage(role="system", content=prompt)])
        return m.content
