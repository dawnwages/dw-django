"""
Spelling help for site search.

The site is small, so instead of a search engine with fuzzy matching we
compare the query against the words in live page titles, descriptions and
tags with difflib. That gives:

* did_you_mean(): the query with misspelled words swapped for close matches
  ("wagtial pupies" -> "wagtail puppies");
* similar_pages(): pages whose titles are near the query, for when search
  finds little or nothing.
"""
import re
from difflib import SequenceMatcher, get_close_matches

from taggit.models import Tag
from wagtail.models import Page

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

# How close a word or title has to be (0-1) to count as a near spelling.
WORD_CUTOFF = 0.75
TITLE_CUTOFF = 0.7


def words(text):
    return WORD.findall((text or "").lower())


def candidate_pages():
    """Live, public pages people can land on (not the tree root)."""
    return (
        Page.objects.live()
        .public()
        .filter(depth__gt=1)
        .only("id", "title", "seo_title", "search_description", "url_path", "content_type")
    )


def vocabulary(pages):
    vocab = set()
    for page in pages:
        for text in (page.title, page.seo_title, page.search_description):
            vocab.update(words(text))
    for name in Tag.objects.values_list("name", flat=True):
        vocab.update(words(name))
    return {w for w in vocab if len(w) > 2}


def did_you_mean(query, vocab):
    """Return the query with misspelled words corrected, or None if nothing changed."""
    corrected, changed = [], False
    known = sorted(vocab)
    for word in words(query):
        if word in vocab or len(word) < 3 or word.isdigit():
            corrected.append(word)
            continue
        match = get_close_matches(word, known, n=1, cutoff=WORD_CUTOFF)
        corrected.append(match[0] if match else word)
        changed = changed or bool(match)
    return " ".join(corrected) if changed else None


def title_score(query_words, title):
    """How close a title is to the query: the better of a whole-string match
    and the average best match for each query word."""
    title_words = words(title)
    if not query_words or not title_words:
        return 0
    whole = SequenceMatcher(None, " ".join(query_words), " ".join(title_words)).ratio()
    per_word = sum(
        max(SequenceMatcher(None, q, t).ratio() for t in title_words) for q in query_words
    ) / len(query_words)
    return max(whole, per_word)


def similar_pages(query, pages, exclude=(), limit=5):
    query_words = [w for w in words(query) if len(w) > 2] or words(query)
    scored = [
        (title_score(query_words, page.title), page)
        for page in pages
        if page.pk not in exclude
    ]
    scored = [item for item in scored if item[0] >= TITLE_CUTOFF]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [page for _, page in scored[:limit]]
