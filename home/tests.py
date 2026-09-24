from datetime import timedelta

from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone
from puput.models import BlogPage, EntryPage
from puput.urls import get_entry_url
from wagtail.models import Page, Site

from home.models import HomePage

# Manifest static storage needs collectstatic, which tests don't run.
PLAIN_STATIC = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


class NewPostAnnouncementTests(TestCase):
    """The home page hero announces blog posts published in the last week."""

    def setUp(self):
        root = Page.get_first_root_node()
        self.home = root.add_child(instance=HomePage(title="Home", slug="test-home", name="Dawn Wages"))
        Site.objects.update_or_create(
            is_default_site=True,
            defaults={"hostname": "localhost", "root_page": self.home, "site_name": "test"},
        )
        self.blog = self.home.add_child(instance=BlogPage(title="Blog", slug="blog"))
        self.request = RequestFactory().get("/", HTTP_HOST="localhost")

    def add_post(self, title, age, live=True):
        return self.blog.add_child(
            instance=EntryPage(
                title=title,
                slug=title.lower().replace(" ", "-"),
                body="<p>Body</p>",
                date=timezone.now() - age,
                live=live,
            )
        )

    def context(self):
        return self.home.get_context(self.request)

    def url(self, post):
        return get_entry_url(post, self.blog.page_ptr, self.home)

    def test_post_from_this_week_is_announced(self):
        post = self.add_post("Fresh post", timedelta(days=1))
        context = self.context()
        self.assertEqual(context["new_posts"], [post])
        self.assertEqual(context["new_posts_count"], 1)

    def test_post_older_than_a_week_is_not_announced(self):
        self.add_post("Old post", timedelta(days=8))
        self.assertEqual(self.context()["new_posts"], [])

    def test_unpublished_posts_are_ignored(self):
        self.add_post("Old post", timedelta(days=8))
        self.add_post("Draft post", timedelta(hours=1), live=False)
        self.assertEqual(self.context()["new_posts_count"], 0)

    def test_all_posts_from_this_week_are_listed_newest_first(self):
        older = self.add_post("Monday post", timedelta(days=5))
        newest = self.add_post("Friday post", timedelta(hours=3))
        middle = self.add_post("Wednesday post", timedelta(days=2))
        self.add_post("Last month post", timedelta(days=30))
        context = self.context()
        self.assertEqual(context["new_posts"], [newest, middle, older])
        self.assertEqual(context["new_posts_count"], 3)
        self.assertEqual(context["new_posts_more"], 0)

    def test_list_is_capped_with_a_count_of_the_rest(self):
        for day in range(5):
            self.add_post(f"Post {day}", timedelta(days=day, hours=1))
        context = self.context()
        self.assertEqual(len(context["new_posts"]), HomePage.NEW_POSTS_SHOWN)
        self.assertEqual(context["new_posts_count"], 5)
        self.assertEqual(context["new_posts_more"], 2)

    @override_settings(STORAGES=PLAIN_STATIC)
    def test_single_post_renders_as_a_pill(self):
        post = self.add_post("Fresh post", timedelta(days=2))
        response = self.client.get("/", HTTP_HOST="localhost")
        self.assertContains(response, "New post")
        self.assertContains(response, f'href="{self.url(post)}"')
        self.assertNotContains(response, "new posts")

    @override_settings(STORAGES=PLAIN_STATIC)
    def test_several_posts_render_as_a_list(self):
        posts = [self.add_post(f"Post {day}", timedelta(days=day, hours=1)) for day in range(4)]
        response = self.client.get("/", HTTP_HOST="localhost")
        self.assertContains(response, "4 new posts")
        for post in posts[:3]:
            self.assertContains(response, f'href="{self.url(post)}"')
        self.assertNotContains(response, f'href="{self.url(posts[3])}"')
        self.assertContains(response, "1 more")
