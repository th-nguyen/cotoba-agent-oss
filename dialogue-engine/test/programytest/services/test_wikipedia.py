"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest
import wikipedia

from programy.services.wikipediaservice import WikipediaService

from programytest.client import TestClient


class MockWikipediaAPI(object):

    DISAMBIGUATIONERROR = 1
    PAGEERROR = 2
    GENERALEXCEPTION = 3

    def __init__(self, response=None, throw_exception=None):
        self._response = response
        self._throw_exception = throw_exception

    def summary(self, title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        if self._throw_exception is not None:
            if self._throw_exception == MockWikipediaAPI.DISAMBIGUATIONERROR:
                raise wikipedia.exceptions.DisambiguationError("Title", "May Refer To")
            elif self._throw_exception == MockWikipediaAPI.PAGEERROR:
                raise wikipedia.exceptions.PageError(pageid=666)
            else:
                raise Exception()
        else:
            return self._response


class WikipediaServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

    def test_ask_question(self):
        service = WikipediaService(api=MockWikipediaAPI(response="Test Wikipedia response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "SUMMARY what is a cat")
        self.assertEqual("Test Wikipedia response", response)

    def test_ask_question_disambiguous(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.DISAMBIGUATIONERROR))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)

    def test_ask_question_pageerror_exception(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.PAGEERROR))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)

    def test_ask_question_general_exception(self):
        service = WikipediaService(api=MockWikipediaAPI(response=None, throw_exception=MockWikipediaAPI.GENERALEXCEPTION))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)
