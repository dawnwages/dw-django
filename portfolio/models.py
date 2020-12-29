from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


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

    