from django import template
from home.models import ProjectIcons, ResumeLink

register = template.Library()


@register.inclusion_tag("includes/icons-footer.html", takes_context=True)
def projecticons(context):
    return {
        "projecticons": ProjectIcons.objects.all()
    }


@register.inclusion_tag("includes/download-resume.html", takes_context=True)
def downloadresume(context):
    return {
        "downloadresume": ResumeLink.objects.last()
    }