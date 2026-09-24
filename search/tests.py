from django.test import TestCase, override_settings
from django.utils import timezone
from wagtail.models import Page, Site

from home.models import GeneralPage
from search import suggest

# Manifest static storage needs collectstatic, which tests don't run.
PLAIN_STATIC = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


class SuggestTests(TestCase):
    def test_misspelled_words_are_corrected(self):
        vocab = {"wagtail", "puppies", "python"}
        self.assertEqual(suggest.did_you_mean("wagtial pupies", vocab), "wagtail puppies")

    def test_known_words_give_no_suggestion(self):
        self.assertIsNone(suggest.did_you_mean("python", {"python"}))

    def test_unrelated_words_are_left_alone(self):
        self.assertIsNone(suggest.did_you_mean("zzzz", {"python"}))

    def test_near_titles_score_above_the_cutoff(self):
        words = suggest.words("talks podcsts")
        self.assertGreaterEqual(suggest.title_score(words, "Talks and Podcasts"), suggest.TITLE_CUTOFF)
        self.assertLess(suggest.title_score(words, "My Puppies"), suggest.TITLE_CUTOFF)


@override_settings(STORAGES=PLAIN_STATIC)
class SearchViewTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home = root.add_child(instance=Page(title="Home", slug="test-home"))
        Site.objects.update_or_create(
            is_default_site=True,
            defaults={"hostname": "localhost", "root_page": self.home, "site_name": "test"},
        )
        self.talks = self.home.add_child(instance=GeneralPage(title="Talks and Podcasts", slug="talks", date=timezone.now()))
        self.home.add_child(instance=GeneralPage(title="My Puppies", slug="my-puppies", date=timezone.now()))

    def get(self, query):
        return self.client.get("/search/", {"query": query}, HTTP_HOST="localhost")

    def test_misspelling_shows_corrected_results(self):
        response = self.get("podcsts")
        self.assertTrue(response.context["showing_corrected"])
        self.assertEqual(response.context["corrected_query"], "podcasts")
        self.assertContains(response, "Talks and Podcasts")

    def test_exact_search_has_no_correction(self):
        response = self.get("podcasts")
        self.assertIsNone(response.context["corrected_query"])
        self.assertFalse(response.context["showing_corrected"])

    def test_similar_pages_exclude_results(self):
        response = self.get("puppies")
        self.assertNotIn(self.talks, response.context["suggested_pages"])
        titles = [r.title for r in response.context["search_results"]]
        self.assertIn("My Puppies", titles)
        self.assertNotIn("My Puppies", [p.title for p in response.context["suggested_pages"]])
