from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from wagtail.models import Site

from home import speaker_rider as rider
from home.models import GeneralPage


class Command(BaseCommand):
    help = (
        "Create or update the Speaker Rider page from home/speaker_rider.py, under the "
        "site's home page. Saves a draft revision unless --publish is given; earlier "
        "versions stay in the page's revision history."
    )

    def add_arguments(self, parser):
        parser.add_argument("--publish", action="store_true", help="Publish instead of saving a draft")
        parser.add_argument("--dry-run", action="store_true", help="Show what would change without saving")

    def handle(self, *args, publish, dry_run, **options):
        site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            raise CommandError("No default site.")
        home = site.root_page

        page = GeneralPage.objects.child_of(home).filter(slug=rider.SLUG).first()
        self.stdout.write(f"{'Updating' if page else 'Creating'} {rider.TITLE} under {home.title} ({home.url_path})")
        if dry_run:
            self.stdout.write("Dry run: nothing saved.")
            return

        if page is None:
            page = GeneralPage(title=rider.TITLE, slug=rider.SLUG, date=timezone.now(), live=False)
            home.add_child(instance=page)
        page = page.get_latest_revision_as_object()
        page.title = rider.TITLE
        page.intro = rider.INTRO
        page.body = rider.BODY
        page.search_description = rider.SEARCH_DESCRIPTION

        revision = page.save_revision(log_action=True)
        if publish:
            revision.publish()
            self.stdout.write(self.style.SUCCESS(f"Published at {page.url_path}"))
        else:
            self.stdout.write(self.style.SUCCESS(
                "Saved as a draft. Review it in the Wagtail admin (Pages > Speaker Rider), then publish."
            ))
