
from opensearchpy import OpenSearch
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
# from django.conf import settings


client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'OneTwo@12'),
    use_ssl=True, 
    verify_certs = False, 
)

@require_GET
def suggestion(request):
    q = request.GET.get('q')
    query = {
        "_source": ["title"],
        "query": {
            "fuzzy": {
                "title": {
                    "value": q,
                    "fuzziness": "AUTO"
                }
            }
        },
        "size": 9
    }
    response = client.search(index="epi-recipes-index", body=query)
    result = [hit["_source"]["title"] for hit in response["hits"]["hits"]]
    titles = {
        "suggestion": result
    }
    
    return JsonResponse(titles)
    





@require_GET
def search_recipes_api(request):
  
    q = request.GET.get('q', '')
    calories_min = request.GET.get('calories_min', None)
    calories_max = request.GET.get('calories_max', None)
    protein_min = request.GET.get('protein_min', None)
    rating_min = request.GET.get('rating_min', None)
    fat_min = request.GET.get('fat_min', None)  
    page = int(request.GET.get('page', 1))  

    query = {
        'size': 300,  
        'query': {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': q,
                            'fields': ['title^2', 'categories', 'ingredients']
                        }
                    }
                ],
                'filter': []  # This will hold the filters
            }
        }
    }


    if calories_min or calories_max:
        calorie_range = {}
        if calories_min:
            calorie_range['gte'] = float(calories_min)
        if calories_max:
            calorie_range['lte'] = float(calories_max)
        query['query']['bool']['filter'].append({
            'range': {
                'calories': calorie_range
            }
        })

    if protein_min:
        query['query']['bool']['filter'].append({
            'range': {
                'protein': {
                    'gte': float(protein_min)
                }
            }
        })

    if rating_min:
        query['query']['bool']['filter'].append({
            'range': {
                'rating': {
                    'gte': float(rating_min)
                }
            }
        })

    if fat_min:
        query['query']['bool']['filter'].append({
            'range': {
                'fat': {
                    'gte': float(fat_min)
                }
            }
        })

    # Search in OpenSearch
    try:
        response = client.search(
            body=query,
            index='epi-recipes-index'
        )
        hits = response['hits']['hits']

        paginator = Paginator(hits, 10)
        paginated_hits = paginator.get_page(page)

        return JsonResponse({
            'results': paginated_hits.object_list,
            'current_page': paginated_hits.number,
            'total_pages': paginated_hits.paginator.num_pages,
            'total_results': paginated_hits.paginator.count
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)