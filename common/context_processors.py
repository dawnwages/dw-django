from puput.models import BlogPage, EntryPage

def draft_entries(request):
    """ Add draft entries to BlogPost index page"""
    blogpage = BlogPage.objects.filter(url_path=request.path)
    #draft_entries = EntryPage.objects.descendant_of(blogpage).filter(has_unpublished_changes=True).order_by('-date').select_related('owner')
    print(request.path)
    print(blogpage)
    return {'draft_entries': 'draft_entries'}