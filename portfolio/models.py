from django.db import models
from django.utils.translation import gettext as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from puput.abstracts import EntryAbstract, BlogAbstract
from puput.utils import get_image_model_path

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel, InlinePanel 
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from portfolio import blocks as dwblocks

class PortfolioTag(TaggedItemBase):
    content_object = ParentalKey(
        'PortfolioEntry',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class PortfolioIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = [
        FieldPanel('intro'),
        FieldPanel('title'),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = PortfolioEntry.objects.child_of(self).order_by('-start_date', 'end_date')

        tag = request.GET.get('tag')
        print(all_posts)
        if tag:
            all_posts = all_posts.filter(tags__name=tag)
        context["posts"] = all_posts
        context["tag"] = tag
        return context


class PortfolioEntry(Page):
    # Options of employment
    FTE = 'FTE'
    CLIENT = 'CLIENT'
    TALK = 'CONFERENCE TALK'
    PROJECT_CHOICES = [
        ('FTE', 'Full Time Engineer'),
        ('CLIENT', 'Client'),
        ('TALK', 'Conference Talk')
    ]
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    current = models.BooleanField(default=False)
    is_case_study = models.BooleanField(default=False)
    client_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    promote_client_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    client_name = models.CharField(max_length=255)
    client_pos = models.CharField(max_length=255)
    client_link = models.URLField(max_length=255, blank=True)
    project_link = models.URLField(max_length=255, blank=True)
    source_link = models.URLField(max_length=255, blank=True)
    client_type = models.CharField(max_length=10, choices=PROJECT_CHOICES, default=FTE)
    client_body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PortfolioTag, blank=True)

    search_fields = Page.search_fields + [
        FieldPanel('current'),
        FieldPanel('client_body', classname="full"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            FieldPanel('current'),
            FieldPanel('tags'),
            FieldPanel('is_case_study'),
        ], heading="Porfolio Info"),
        FieldPanel('client_name'),
        FieldPanel('client_pos'),
        FieldPanel('client_link'),
        FieldPanel('project_link'),
        FieldPanel('source_link'),
        FieldPanel('client_type'),
        FieldPanel('client_body'),
        ImageChooserPanel('client_logo'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('promote_client_logo'),
    ]

    parent_page_types = ['portfolio.PortfolioIndexPage']
    subpage_types = []


class DWEntryAbstract(EntryAbstract):
    content = StreamField(
        [
            ("heading", dwblocks.HeadingBlock(class_name="full")),
            ("subheading", blocks.CharBlock(class_name="full")),
            ("paragraph", blocks.RichTextBlock()),
            ("html", blocks.RawHTMLBlock(icon="code", label="Raw HTML")),
            ("image", ImageChooserBlock()),
            ("text_with_heading", dwblocks.TextWithHeadingBlock(class_name="full")),
            ("text_with_heading_and_right_image", dwblocks.TextWithHeadingWithRightImageBlock(class_name="full")),
            ("text_with_heading_and_left_image", dwblocks.TextWithHeadingWithLeftImageBlock(class_name="full")),
            ("right_image_left_text", dwblocks.RightImageLeftTextBlock(class_name="full")),
            ("left_image_right_text", dwblocks.LeftImageRightTextBlock(class_name="full")),
            ("left_quote_right_image", dwblocks.QuoteLeftImageBlock(class_name="full")),
            ("video_embed", dwblocks.LiteYoutubeEmbed(class_name="full")),
            ("table", TableBlock(class_name="full")),
        ],
        blank=True,
        null=True,
    )
    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title', classname="title"),
                ImageChooserPanel('header_image'),
                FieldPanel('body', classname="full"),
                StreamFieldPanel("content"),
                FieldPanel('excerpt', classname="full"),
            ],
            heading=_("Content")
        ),
        MultiFieldPanel(
            [
                FieldPanel('tags'),
                InlinePanel('entry_categories', label=_("Categories")),
                InlinePanel(
                    'related_entrypage_from',
                    label=_("Related Entries"),
                    panels=[PageChooserPanel('entrypage_to')]
                ),
            ],
            heading=_("Page Metadata")),
    ]

    class Meta:
        abstract = True