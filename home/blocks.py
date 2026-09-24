from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

STYLE_GUIDE_COLORS = (
    ("red", "red"),
    ("blue", "blue"),
    ("yellow", "yellow"),
)

CODE_LANGUAGE_OPTIONS = (
    ("Python", "python"),
    ("Markup", "html"),
    ("CSS", "css"),
    ("Clojure", "clojure"),
    ("Bash", "shell"),
    ("Django", "django"),
    ("Jinja2", "jinja2"),
    ("Docker", "dockerfile"),
    ("Git", "git"),
    ("GraphQL", "graphql"),
    ("Handlebars", "handlebars"),
    (".ignore", "gitignore"),
    ("JSON", "json"),
    ("JSON5", "json5"),
    ("Markdown", "md"),
    ("Markdown", "md"),
    ("React JSX", "jsx"),
    ("React TSX", "tsx"),
    ("SASS", "sass"),
    ("SCSS", "scss"),
    ("TypeScript", "ts"),
    ("vim", "vim"),
)


class HeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)

    def __str__(self):
        return self.heading

    class Meta:
        template = "home/blocks/heading.html"


class TextWithHeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    text = blocks.TextBlock()

    def __str__(self):
        return self.heading

    class Meta:
        label = "Text Block with Header"
        template = "home/blocks/text-with-heading.html"


class TextWithHeadingWithRightImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    text = blocks.TextBlock()
    image = ImageChooserBlock()

    def __str__(self):
        return self.heading

    class Meta:
        label = "Text Block with Header: Right Image"
        template = "cms/blocks/text-with-heading-right-image.html"


class TextHeadingImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    text = blocks.TextBlock()
    image = ImageChooserBlock()
    # TODO: Add left or right side

    def __str__(self):
        return self.heading

    class Meta:
        label = "Text, Header and Image"
        template = "home/blocks/text-image-heading.html"


class VideoEmbed(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    text = blocks.TextBlock()
    # TODO: Add color and embed field

    def __str__(self):
        return self.heading

    class Meta:
        label = "Video Embed"
        template = "home/blocks/video-embed.html"


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=CODE_LANGUAGE_OPTIONS)
    caption = blocks.CharBlock(max_length=255, blank=True)
    page = blocks.CharBlock(max_length=255, blank=True)
    code = blocks.TextBlock(max_length=1000, blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        label = "Code Block"
        template = "home/blocks/code-block.html"


class QuoteBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255)
    attribution = blocks.CharBlock(max_length=255)

    def __str__(self):
        return self.attribution

    class Meta:
        label = "Quote Block"
        template = "home/blocks/quote-block.html"


# ---------------------------------------------------------------------------
# Talks and podcasts
# ---------------------------------------------------------------------------

TALK_KINDS = [
    ("keynote", "Keynote"),
    ("talk", "Talk"),
    ("panel", "Panel"),
    ("fireside", "Fireside chat"),
    ("workshop", "Workshop"),
    ("podcast", "Podcast"),
    ("interview", "Video interview"),
]

# Filter groups shown above the list: (key, label, kinds).
TALK_FILTERS = [
    ("keynotes", "Keynotes", {"keynote"}),
    ("talks", "Talks & panels", {"talk", "panel", "fireside", "workshop"}),
    ("media", "Podcasts & interviews", {"podcast", "interview"}),
]


class TalkLinkBlock(blocks.StructBlock):
    kind = blocks.ChoiceBlock(
        choices=[
            ("watch", "Watch"),
            ("listen", "Listen"),
            ("slides", "Slides"),
            ("transcript", "Transcript"),
            ("details", "Details"),
        ],
        default="details",
    )
    url = blocks.URLBlock()
    label = blocks.CharBlock(required=False, max_length=80, help_text="Defaults to the link type")


class TalkValue(blocks.StructValue):
    def filter_group(self):
        return next((key for key, _, kinds in TALK_FILTERS if self.get("kind") in kinds), "talks")


class TalkBlock(blocks.StructBlock):
    kind = blocks.ChoiceBlock(choices=TALK_KINDS, default="talk")
    title = blocks.CharBlock(max_length=255)
    event = blocks.CharBlock(max_length=255, help_text="e.g. DjangoCon US 2026, or the podcast name")
    location = blocks.CharBlock(required=False, max_length=120)
    date = blocks.DateBlock(required=False)
    date_precision = blocks.ChoiceBlock(
        choices=[("day", "Day"), ("month", "Month"), ("year", "Year only")],
        default="day",
        help_text="How much of the date to show",
    )
    with_people = blocks.CharBlock(required=False, max_length=255, help_text="e.g. with Tereza Iofciu and Jessica Greene")
    description = blocks.TextBlock(required=False)
    links = blocks.ListBlock(TalkLinkBlock(), default=[])
    featured = blocks.BooleanBlock(required=False, help_text="Highlight at the top of the page")

    class Meta:
        value_class = TalkValue


class TalksValue(blocks.StructValue):
    def featured(self):
        return next((talk for talk in self.get("talks") if talk.get("featured")), None)

    def by_year(self):
        """[(year, talks)] newest first, excluding the featured talk shown above the
        list; talks without a date go last under "Earlier"."""
        featured = self.featured()
        talks = [t for t in self.get("talks") if t is not featured]
        dated = sorted((t for t in talks if t.get("date")), key=lambda t: t["date"], reverse=True)
        groups = {}
        for talk in dated:
            groups.setdefault(str(talk["date"].year), []).append(talk)
        undated = [t for t in talks if not t.get("date")]
        return list(groups.items()) + ([("Earlier", undated)] if undated else [])

    def filters(self):
        present = {talk.filter_group() for talk in self.get("talks")}
        return [(key, label) for key, label, _ in TALK_FILTERS if key in present]


class TalksBlock(blocks.StructBlock):
    talks = blocks.ListBlock(TalkBlock())

    class Meta:
        icon = "microphone"
        label = "Talks and podcasts"
        value_class = TalksValue
        template = "home/blocks/talks.html"
