import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase, override_settings
from puput.models import BlogPage, EntryPage
from wagtail.models import Page, Site

from home.management.commands.publish_posts import body_to_blocks, parse_post
from home.models import HomePage

PLAIN_STATIC = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

POST = """---
title: A Test Post
slug: a-test-post
date: 2026-10-17
tags: AI, Agents
excerpt: Short summary.
---

Intro paragraph with a [link](https://example.com).

## First section

Some prose.

```python
print("hi")
```

More prose.
"""


class ParseTests(TestCase):
    def test_frontmatter(self):
        meta, body = parse_post(POST)
        self.assertEqual(meta["title"], "A Test Post")
        self.assertEqual(meta["slug"], "a-test-post")
        self.assertEqual(meta["tags"], ["AI", "Agents"])
        self.assertTrue(body.startswith("Intro paragraph"))

    def test_blocks(self):
        _, body = parse_post(POST)
        types = [block["type"] for block in body_to_blocks(body)]
        self.assertEqual(types, ["prose", "section_heading", "prose", "tech_code", "prose"])


@override_settings(STORAGES=PLAIN_STATIC)
class PublishPostsTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        home = root.add_child(instance=HomePage(title="Home", slug="test-home", name="Dawn Wages"))
        Site.objects.update_or_create(
            is_default_site=True, defaults={"hostname": "localhost", "root_page": home, "site_name": "test"}
        )
        self.blog = home.add_child(instance=BlogPage(title="Blog", slug="blog"))
        self.dir = tempfile.TemporaryDirectory()
        Path(self.dir.name, "a-test-post.md").write_text(POST, encoding="utf-8")

    def tearDown(self):
        self.dir.cleanup()

    def publish(self, *args):
        call_command("publish_posts", "--dir", self.dir.name, *args, stdout=open("/dev/null", "w"))

    def test_publishes_new_post(self):
        self.publish()
        post = EntryPage.objects.child_of(self.blog).get(slug="a-test-post")
        self.assertTrue(post.live)
        self.assertEqual(post.title, "A Test Post")
        self.assertEqual(sorted(t.name for t in post.tags.all()), ["AI", "Agents"])
        self.assertEqual([b.block_type for b in post.content][0], "prose")

    def test_existing_post_is_left_alone(self):
        self.publish()
        post = EntryPage.objects.get(slug="a-test-post")
        post.title = "Edited in admin"
        post.save_revision().publish()
        self.publish()
        self.assertEqual(EntryPage.objects.get(slug="a-test-post").title, "Edited in admin")
        self.assertEqual(EntryPage.objects.filter(slug="a-test-post").count(), 1)

    def test_update_overwrites(self):
        self.publish()
        post = EntryPage.objects.get(slug="a-test-post")
        post.title = "Edited in admin"
        post.save_revision().publish()
        self.publish("--update")
        self.assertEqual(EntryPage.objects.get(slug="a-test-post").title, "A Test Post")
