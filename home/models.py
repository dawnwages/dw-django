from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from portfolio.models import PortfolioTag


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


class GeneralPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=GeneralTag, blank=True)
    date = models.DateTimeField("Post Date")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Page Information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery Image"),
        ]


class GeneralPageGalleryImage(Orderable):
    page = ParentalKey(GeneralPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


@register_snippet
class ProjectIcons(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
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
        DocumentChooserPanel('resume')
    ]

    def __str__(self):
        return self.title
