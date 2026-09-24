from django import template
from django.db.models import Count, Q
from el_pagination.templatetags.el_pagination_tags import get_pages
from puput.models import Category
from taggit.models import Tag

register = template.Library()

# puput registers el_pagination's paginate/show_paginator without installing
# the app; expose get_pages the same way so templates can build custom pagers.
register.tag("get_pages", get_pages)


@register.simple_tag
def blog_topics(blog_page, limit=None):
    """Tags used by live posts in this blog, most used first, with num_posts."""
    live_in_blog = Q(
        puput_tagentrypage_items__content_object__live=True,
        puput_tagentrypage_items__content_object__path__startswith=blog_page.path,
    )
    tags = (
        Tag.objects.filter(live_in_blog)
        .annotate(num_posts=Count("puput_tagentrypage_items", filter=live_in_blog, distinct=True))
        .order_by("-num_posts", "name")
    )
    return tags[:limit] if limit else tags


@register.simple_tag
def blog_categories(blog_page):
    """Categories used by live posts in this blog, most used first, with num_posts."""
    live_in_blog = Q(entrypage__live=True, entrypage__path__startswith=blog_page.path)
    return (
        Category.objects.filter(live_in_blog)
        .annotate(num_posts=Count("entrypage", filter=live_in_blog, distinct=True))
        .order_by("-num_posts", "name")
    )
