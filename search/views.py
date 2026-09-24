from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

from search import suggest

# Below this many results, also suggest pages with similar titles.
FEW_RESULTS = 3


def run_search(query):
    return Page.objects.live().public().search(query)


def search(request):
    search_query = (request.GET.get('query') or '').strip()
    page = request.GET.get('page', 1)
    corrected_query = None       # "Did you mean …?"
    showing_corrected = False    # results are for corrected_query, not search_query
    suggested_pages = []

    if search_query:
        search_results = run_search(search_query)
        Query.get(search_query).add_hit()

        pages = list(suggest.candidate_pages())
        corrected_query = suggest.did_you_mean(search_query, suggest.vocabulary(pages))
        if corrected_query and not search_results.count():
            corrected_results = run_search(corrected_query)
            if corrected_results.count():
                search_results = corrected_results
                showing_corrected = True

        if search_results.count() < FEW_RESULTS:
            found = {result.pk for result in search_results}
            suggested_pages = suggest.similar_pages(
                corrected_query or search_query, pages, exclude=found
            )
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'result_count': paginator.count,
        'corrected_query': corrected_query,
        'showing_corrected': showing_corrected,
        'suggested_pages': suggested_pages,
    })
