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
