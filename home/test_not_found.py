import importlib
import os
from unittest import mock

from django.test import TestCase, override_settings

PLAIN_STATIC = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


@override_settings(STORAGES=PLAIN_STATIC, DEBUG=False)
class NotFoundPageTests(TestCase):
    def test_missing_page_shows_friendly_404(self):
        response = self.client.get("/no-such-page-here/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        html = response.content.decode()
        self.assertIn("Oops, no page here", html)
        self.assertIn("/no-such-page-here/", html)
        self.assertIn('action="/search/"', html)
        for href in ("/talks-and-podcasts/", "/bajoran-engineer/", "/star-trek-themed-demos/"):
            self.assertIn(f'href="{href}"', html)


class DebugFlagTests(TestCase):
    """The deploy settings must treat DEBUG=False (as Heroku sets it) as off."""

    def debug_for(self, value):
        from dawnwagesinfo.settings import deploy
        env = {"DEBUG": value} if value is not None else {}
        with mock.patch.dict(os.environ, env, clear=False):
            if value is None:
                os.environ.pop("DEBUG", None)
            with mock.patch("dotenv.load_dotenv"):
                return importlib.reload(deploy).DEBUG

    def test_false_text_is_off(self):
        for value in ("False", "false", "0", "", None):
            self.assertFalse(self.debug_for(value), value)

    def test_true_text_is_on(self):
        for value in ("True", "true", "1"):
            self.assertTrue(self.debug_for(value), value)
