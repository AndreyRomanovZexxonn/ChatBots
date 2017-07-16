# -*- coding: utf-8 -*-
__author__ = 'zexxonn'

import wikipedia as wiki
import urllib

MLWordsDictionary = set(["gradient", "boosting", "machine", "learning"])

class WikiHandler(object):

    @staticmethod
    def request(text):
        lang = 'en'
        wiki.set_lang(lang)
        preparedText = text.lower().strip()
        words = preparedText.split(" ")

        searchQuery = " ".join([w for w in words if w in MLWordsDictionary])
        if not searchQuery:
            return "Can't find relevant page."

        searchResult = wiki.search(searchQuery, results=1, suggestion=False)
        searchPage = wiki.page(searchResult[0]) if searchResult else None

        if not searchPage:
            return "Can't find relevant page."

        if lang == 'ru':
            url = urllib.unquote(searchPage.url.encode("utf-8"))
            return url.decode("utf-8")

        return searchPage.url