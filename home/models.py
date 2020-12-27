from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


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
