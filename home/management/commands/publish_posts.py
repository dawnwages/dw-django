"""Publish Markdown posts from posts/ as blog entries.

Each file in posts/ is one post: a frontmatter block between `---` lines, then
the body in Markdown. Frontmatter keys are `key: value` lines:

    ---
    title: Human-in-the-Loop Isn't Enough
    slug: human-in-the-loop-isnt-enough
    date: 2026-10-17
    tags: AI, Agents, Domain-Driven Design
    excerpt: One or two sentences for listings and link previews.
    ---

The body becomes the entry's content StreamField: `## ` lines become section
headings (so the post gets an "On this page" menu), fenced code becomes code
blocks, and everything between them becomes prose.

Runs in the Heroku release phase after migrate. A post that already exists is
left alone, so edits made in the Wagtail admin are never overwritten; pass
--update to push a file's content over the live page.
"""

import datetime
import json
import re
from pathlib import Path

import markdown
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify
from puput.models import BlogPage, EntryPage

POSTS_DIR = Path(settings.BASE_DIR) / "posts"
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n(.*)\Z", re.DOTALL)


def parse_post(text):
    match = FRONTMATTER.match(text.replace("\r\n", "\n").lstrip("﻿"))
    if not match:
        raise ValueError("no frontmatter: the file must open with a '---' block")
    meta = {}
    for line in match.group(1).splitlines():
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()
    if not meta.get("title"):
        raise ValueError("frontmatter needs a title")
    meta["slug"] = meta.get("slug") or slugify(meta["title"])
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    return meta, match.group(2).strip()


def body_to_blocks(body):
    blocks, prose, lines, i = [], [], body.split("\n"), 0

    def flush():
        text = "\n".join(prose).strip()
        if text:
            blocks.append({"type": "prose", "value": markdown.markdown(text)})
        prose.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            flush()
            blocks.append(
                {"type": "section_heading", "value": {"text": line[3:].strip(), "level": "h2", "anchor": ""}}
            )
        elif line.startswith("```"):
            flush()
            language = line[3:].strip() or "none"
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(
                {
                    "type": "tech_code",
                    "value": {
                        "filename": "",
                        "language": language,
                        "code": "\n".join(code),
                        "highlight_lines": "",
                        "show_diff": False,
                        "line_numbers": False,
                        "caption": "",
                    },
                }
            )
        else:
            prose.append(line)
        i += 1
    flush()
    return blocks


def post_date(value):
    if not value:
        return timezone.now()
    day = datetime.date.fromisoformat(value)
    return timezone.make_aware(datetime.datetime(day.year, day.month, day.day, 9, 0))


class Command(BaseCommand):
    help = "Publish the Markdown posts in posts/ as blog entries. Existing posts are skipped unless --update."

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Overwrite posts that already exist")
        parser.add_argument("--dry-run", action="store_true", help="Show what would happen without saving")
        parser.add_argument("--dir", default=str(POSTS_DIR), help="Folder of Markdown posts")

    def handle(self, *args, update, dry_run, dir, **options):
        folder = Path(dir)
        files = sorted(folder.glob("*.md"))
        if not files:
            self.stdout.write(f"No posts in {folder}.")
            return

        blog = BlogPage.objects.live().first()
        if blog is None:
            raise CommandError("No live blog page to publish under.")

        for path in files:
            try:
                meta, body = parse_post(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                raise CommandError(f"{path.name}: {exc}")

            existing = EntryPage.objects.child_of(blog).filter(slug=meta["slug"]).first()
            if existing and not update:
                self.stdout.write(f"Skipped {meta['slug']} (already exists)")
                continue

            blocks = body_to_blocks(body)
            action = "Updated" if existing else "Published"
            if dry_run:
                self.stdout.write(f"Would publish {meta['slug']}: {len(blocks)} blocks, tags {meta['tags']}")
                continue

            if existing:
                page = existing.specific.get_latest_revision_as_object()
            else:
                page = EntryPage(title=meta["title"], slug=meta["slug"], date=post_date(meta.get("date")), live=False)
                blog.add_child(instance=page)
                page = EntryPage.objects.get(pk=page.pk)

            page.title = meta["title"]
            page.excerpt = f"<p>{meta['excerpt']}</p>" if meta.get("excerpt") else ""
            page.body = ""
            page.content = json.dumps(blocks)
            page.tags.clear()
            page.tags.add(*meta["tags"])
            page.save_revision(log_action=True).publish()
            self.stdout.write(self.style.SUCCESS(f"{action} {page.title} ({page.url_path})"))
