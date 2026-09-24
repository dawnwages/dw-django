"""
StreamField blocks for technical blog posts.

Modelled on the elements that recur across well-regarded technical blogs
(Cloudflare, Josh W. Comeau, Julia Evans, Simon Willison): anchored section
headings that feed a table of contents, code with filenames, line highlights
and copy buttons, terminal sessions, tabbed code, callouts, captioned figures,
diagrams, math, summaries, collapsible details, pull quotes and references.

Templates live in templates/blocks/tech/. Front-end behaviour (copy buttons,
tabs, Mermaid, KaTeX) is in static/js/blog.js; syntax highlighting is Prism,
loaded from the CDN in templates/base.html. No build step.
"""
from django.utils.text import slugify
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

GROUP = "Technical writing"

# Prism language ids (values) with editor-friendly labels.
LANGUAGE_CHOICES = [
    ("python", "Python"),
    ("bash", "Bash / shell"),
    ("shell-session", "Shell session (with output)"),
    ("json", "JSON"),
    ("yaml", "YAML"),
    ("toml", "TOML"),
    ("ini", "INI / .cfg"),
    ("sql", "SQL"),
    ("django", "Django / Jinja template"),
    ("markup", "HTML / XML"),
    ("css", "CSS"),
    ("javascript", "JavaScript"),
    ("typescript", "TypeScript"),
    ("jsx", "JSX"),
    ("tsx", "TSX"),
    ("docker", "Dockerfile"),
    ("nginx", "nginx"),
    ("http", "HTTP"),
    ("graphql", "GraphQL"),
    ("markdown", "Markdown"),
    ("rust", "Rust"),
    ("go", "Go"),
    ("c", "C"),
    ("cpp", "C++"),
    ("diff", "Diff (plain)"),
    ("none", "Plain text"),
]

INLINE_FEATURES = ["bold", "italic", "link", "code", "strikethrough", "superscript", "subscript"]
PROSE_FEATURES = INLINE_FEATURES + ["ol", "ul", "blockquote", "hr"]


class SectionHeadingValue(blocks.StructValue):
    def anchor(self):
        return slugify(self.get("anchor") or self.get("text"))

    @property
    def anchor_id(self):
        # Templates can't call anchor(): StructValue is a dict, so {{ value.anchor }}
        # resolves to the raw (often empty) "anchor" field before the method.
        return self.anchor()


class SectionHeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255)
    level = blocks.ChoiceBlock(
        choices=[("h2", "Section (H2)"), ("h3", "Subsection (H3)")],
        default="h2",
    )
    anchor = blocks.CharBlock(
        required=False,
        max_length=80,
        help_text="Optional link slug. Defaults to the heading text.",
    )

    class Meta:
        icon = "title"
        label = "Section heading"
        group = GROUP
        value_class = SectionHeadingValue
        template = "blocks/tech/section_heading.html"


class ProseBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        super().__init__(features=PROSE_FEATURES, **kwargs)

    class Meta:
        icon = "pilcrow"
        label = "Prose"
        group = GROUP
        template = "blocks/tech/prose.html"


class CodeBlock(blocks.StructBlock):
    filename = blocks.CharBlock(
        required=False, max_length=255, help_text="Shown in the code header, e.g. app/models.py"
    )
    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, default="python")
    code = blocks.TextBlock()
    highlight_lines = blocks.CharBlock(
        required=False, max_length=100, help_text="Lines to emphasise, e.g. 3 or 2,5-7"
    )
    show_diff = blocks.BooleanBlock(
        required=False,
        help_text="Treat lines starting with + or - as added or removed, keeping syntax colours.",
    )
    line_numbers = blocks.BooleanBlock(required=False)
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "code"
        label = "Code"
        group = GROUP
        template = "blocks/tech/code.html"


class TerminalBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=100, help_text="e.g. Terminal, zsh")
    prompt = blocks.CharBlock(default="$", max_length=20)
    commands = blocks.TextBlock(help_text="One command per line.")
    output = blocks.TextBlock(required=False)

    class Meta:
        icon = "cogs"
        label = "Terminal session"
        group = GROUP
        template = "blocks/tech/terminal.html"


class CodeTabBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=40, help_text="Tab label, e.g. Python, Before, After")
    filename = blocks.CharBlock(required=False, max_length=255)
    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, default="python")
    code = blocks.TextBlock()


class CodeTabsBlock(blocks.StructBlock):
    tabs = blocks.ListBlock(CodeTabBlock(), min_num=2)
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "list-ul"
        label = "Tabbed code"
        group = GROUP
        template = "blocks/tech/code_tabs.html"


class CalloutBlock(blocks.StructBlock):
    kind = blocks.ChoiceBlock(
        choices=[
            ("note", "Note"),
            ("tip", "Tip"),
            ("important", "Important"),
            ("warning", "Warning"),
            ("caution", "Caution"),
        ],
        default="note",
    )
    title = blocks.CharBlock(required=False, max_length=120, help_text="Defaults to the kind, e.g. Note")
    body = blocks.RichTextBlock(features=PROSE_FEATURES)

    class Meta:
        icon = "warning"
        label = "Callout"
        group = GROUP
        template = "blocks/tech/callout.html"


class FigureBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text = blocks.CharBlock(
        required=False, max_length=255, help_text="Describe the image. Defaults to the image title."
    )
    caption = blocks.RichTextBlock(required=False, features=INLINE_FEATURES)
    credit = blocks.CharBlock(required=False, max_length=255)
    width = blocks.ChoiceBlock(
        choices=[("content", "Text width"), ("wide", "Wide")], default="content"
    )

    class Meta:
        icon = "image"
        label = "Figure"
        group = GROUP
        template = "blocks/tech/figure.html"


class DiagramBlock(blocks.StructBlock):
    source = blocks.TextBlock(help_text="Mermaid syntax, e.g. flowchart LR; A-->B")
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "site"
        label = "Diagram (Mermaid)"
        group = GROUP
        template = "blocks/tech/diagram.html"


class MathBlock(blocks.StructBlock):
    latex = blocks.TextBlock(help_text=r"LaTeX, without $$ delimiters, e.g. t = b \cdot 2^n")
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "doc-full"
        label = "Equation"
        group = GROUP
        template = "blocks/tech/math.html"


class SummaryBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[
            ("tldr", "TL;DR"),
            ("prerequisites", "Before you start"),
            ("takeaways", "Key takeaways"),
        ],
        default="tldr",
    )
    items = blocks.ListBlock(blocks.RichTextBlock(features=INLINE_FEATURES))

    class Meta:
        icon = "list-ol"
        label = "Summary list"
        group = GROUP
        template = "blocks/tech/summary.html"


class DetailsBlock(blocks.StructBlock):
    summary = blocks.CharBlock(max_length=255, help_text="The always-visible line")
    body = blocks.RichTextBlock(features=PROSE_FEATURES)
    open = blocks.BooleanBlock(required=False, help_text="Expanded by default")

    class Meta:
        icon = "collapse-down"
        label = "Collapsible details"
        group = GROUP
        template = "blocks/tech/details.html"


class PullQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    attribution = blocks.CharBlock(required=False, max_length=255)
    source_url = blocks.URLBlock(required=False)

    class Meta:
        icon = "openquote"
        label = "Pull quote"
        group = GROUP
        template = "blocks/tech/pull_quote.html"


class ReferenceBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    url = blocks.URLBlock()
    note = blocks.CharBlock(required=False, max_length=255)


class ReferencesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(default="Further reading", max_length=100)
    items = blocks.ListBlock(ReferenceBlock())

    class Meta:
        icon = "link"
        label = "References"
        group = GROUP
        template = "blocks/tech/references.html"


class CaptionedEmbedBlock(blocks.StructBlock):
    embed = EmbedBlock(help_text="URL of a video, gist, slide deck or other oEmbed provider")
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "media"
        label = "Embed"
        group = GROUP
        template = "blocks/tech/embed.html"


TECH_BLOCKS = [
    ("section_heading", SectionHeadingBlock()),
    ("prose", ProseBlock()),
    ("tech_code", CodeBlock()),
    ("terminal", TerminalBlock()),
    ("code_tabs", CodeTabsBlock()),
    ("callout", CalloutBlock()),
    ("figure", FigureBlock()),
    ("diagram", DiagramBlock()),
    ("math", MathBlock()),
    ("summary", SummaryBlock()),
    ("details", DetailsBlock()),
    ("pull_quote", PullQuoteBlock()),
    ("references", ReferencesBlock()),
    ("embed", CaptionedEmbedBlock()),
]
