from django.shortcuts import render
import json
from django.http import JsonResponse

def search_page(request):
    return render(request, 'search/search_page.html')

def search_results(request):
    query = request.GET.get('query', '').lower()
    
    with open('cocktail_data.json', 'r', encoding='utf-8') as f:
        cocktail_data = json.load(f)
    
    results = []
    for cocktail in cocktail_data:
        for name, details in cocktail.items():
            # substitutes 필드를 제외하고 검색
            filtered_details = {k: v for k, v in details.items() if k != 'substitutes'}
            
            if query in name.lower() or any(query in str(value).lower() for value in filtered_details.values()):
                # 추가 정보를 extra_info 필드에 저장 (Base Liquor, Glass, Strength 이외의 검색된 값을 저장)
                extra_info = []
                if query in str(details.get('garnish', '')).lower():
                    extra_info.append(f'Garnish: {details.get("garnish", "")}')
                if query in str(details.get('ingredients', '')).lower():
                    extra_info.append(f'Ingredients: {details.get("ingredients", "")}')
                if query in str(details.get('recipe', '')).lower():
                    extra_info.append(f'Recipe: {details.get("recipe", "")}')
                if query in str(details.get('tip', '')).lower():
                    extra_info.append(f'Tip: {details.get("tip", "")}')
                
                results.append({
                    'name': name,
                    'base_liquor': details.get('base_liquor', 'Unknown'),
                    'glass': details.get('glass', 'Unknown'),
                    'alcohol_strength': details.get('alcohol_strength', 'Unknown'),
                    'extra_info': ', '.join(extra_info) if extra_info else None  # 추가 정보를 extra_info에 저장
                })
    
    # 칵테일 이름을 기준으로 알파벳 순으로 정렬
    sorted_results = sorted(results, key=lambda x: x['name'].lower())

    return JsonResponse({'results': sorted_results})
