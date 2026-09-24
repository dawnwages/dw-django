from django.core.management.base import BaseCommand, CommandError

from home.models import GeneralPage
from home.talks_data import TALKS

INTRO = (
    "<p>Keynotes, talks, panels and podcasts on Python, AI, open-source governance "
    "and building inclusive communities.</p>"
)
# The tags the live page already had; added when the page has none.
TAGS = ["Talks", "Pycon", "Podcast"]


def talk_value(talk):
    return {
        "kind": talk["kind"],
        "title": talk["title"],
        "event": talk["event"],
        "location": talk.get("location", ""),
        "date": talk.get("date"),
        "date_precision": talk.get("date_precision", "day"),
        "with_people": talk.get("with_people", ""),
        "description": talk.get("description", ""),
        "links": [{"kind": kind, "url": url, "label": label} for kind, url, label in talk.get("links", [])],
        "featured": talk.get("featured", False),
    }


class Command(BaseCommand):
    help = (
        "Replace the Talks and Podcasts page content with a Talks block built from "
        "home/talks_data.py. Saves a draft revision unless --publish is given; the "
        "previous content stays in the page's revision history."
    )

    def add_arguments(self, parser):
        parser.add_argument("--slug", default="talks-and-podcasts", help="Slug of the page to update")
        parser.add_argument("--publish", action="store_true", help="Publish instead of saving a draft")
        parser.add_argument("--dry-run", action="store_true", help="Show what would change without saving")

    def handle(self, *args, slug, publish, dry_run, **options):
        page = GeneralPage.objects.filter(slug=slug).first()
        if page is None:
            raise CommandError(f"No general page with slug {slug!r}.")
        page = page.get_latest_revision_as_object()

        old_blocks = [block.block_type for block in page.content or []]
        self.stdout.write(f"Page: {page.title} ({page.url_path})")
        self.stdout.write(f"Replacing {len(old_blocks)} content block(s): {', '.join(old_blocks) or 'none'}")
        self.stdout.write(f"With {len(TALKS)} talks in one Talks block.")
        if dry_run:
            self.stdout.write("Dry run: nothing saved.")
            return

        page.content = [("talks", {"talks": [talk_value(talk) for talk in TALKS]})]
        if not page.intro:
            page.intro = INTRO
        if not page.tags.exists():
            page.tags.add(*TAGS)
        revision = page.save_revision(log_action=True)
        if publish:
            revision.publish()
            self.stdout.write(self.style.SUCCESS("Published."))
        else:
            self.stdout.write(self.style.SUCCESS(
                "Saved as a draft. Review it in the Wagtail admin (Pages > Talks and Podcasts), then publish."
            ))
