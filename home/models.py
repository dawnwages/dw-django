from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
# from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from portfolio.models import PortfolioTag
from home import blocks as dblocks


class HomePage(Page):
    name = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    desc = models.CharField(max_length=255, blank=True)
    loc = models.CharField(max_length=255, blank=True)
    desc_long = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('desc'),
        FieldPanel('loc'),
        FieldPanel('desc_long', classname="full")
    ]


class GeneralTag(TaggedItemBase):
    content_object = ParentalKey(
        'GeneralPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

# We are not currently using this model. Instead we're using directly the Image chooser panel
# @register_snippet
class GeneralPageGalleryImage(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

    class Meta:
        verbose_name = "Gallery Page Image"


class GalleryBlock(Orderable):
    title = models.CharField(max_length=255)
    gallery = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    related_page = ParentalKey(
        'wagtailcore.Page',
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Pick gallery images",
        related_name="gallery_carousel"
    )

    panels = [
        FieldPanel('title'),
        FieldPanel("gallery")

    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Gallery Carousel"
        ordering = ['sort_order']


class GalleryChooserBlock(blocks.StructBlock):
    gallery = ImageChooserBlock("home.GalleryBlock")


    def __str__(self):
        return self.gallery


class GeneralPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=GeneralTag, blank=True)
    date = models.DateTimeField("Post Date")
    content = StreamField(
        [
            ("heading", dblocks.HeadingBlock(class_name="full")),
            ("subheading", blocks.CharBlock(class_name="full")),
            ("paragraph", blocks.RichTextBlock(class_name="full")),
            ("HTML", blocks.RawHTMLBlock(class_name="full")),
            ("image", ImageChooserBlock()),
            ("text_with_heading", dblocks.HeadingBlock(class_name="full")),
            ("text_heading_image", dblocks.TextHeadingImageBlock(class_name="full")),
            ("video_embed", dblocks.VideoEmbed(class_name="full")),
            ("table", TableBlock(class_name="full")),
            ("code_block", dblocks.CodeBlock(class_name="full")),
            ("quote_block", dblocks.QuoteBlock(class_name="full")),
            ("gallery_chooser", GalleryChooserBlock(class_name="full"))
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Page Information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel("content"),
        InlinePanel('gallery_carousel', label="gallery", min_num=1, max_num=10)
        ]


@register_snippet
class ProjectIcons(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return self.caption


@register_snippet
class ResumeLink(models.Model):
    title = models.CharField(max_length=255)
    resume = models.ForeignKey(
        'wagtaildocs.Document',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    upload_date = models.DateTimeField(auto_now_add=True, null=True)

    panels = Page.content_panels + [
        FieldPanel('resume')
    ]

    def __str__(self):
        return self.title
