
import random
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import os
import traceback
from .models import UserProfile


# Create your views here.

from cocktail.models import Cocktail  # Cocktail 모델을 가져옴

def main_page(request):
    return render(request, 'main/main_page.html')

def my_page(request):
    profile = UserProfile.objects.get(user=request.user)

    return render(request, 'main/my_page.html', {
        'base_liquor': profile.base_liquor,
        'alcohol_strength': profile.alcohol_strength,
        'glass': profile.glass,
        'technique': profile.technique,
    })

def recommend_cocktails(request):
    if request.method == 'POST':
        try:
            # POST 요청에서 카테고리 데이터 가져오기
            category = request.POST.get('category')

            # JSON 파일 경로 지정
            json_file_path = os.path.join(settings.BASE_DIR, 'cocktail_data.json')

            # JSON 파일 존재 여부 확인
            if not os.path.exists(json_file_path):
                return JsonResponse({'error': 'JSON 파일을 찾을 수 없습니다.'}, status=500)

            # JSON 데이터 불러오기
            with open(json_file_path, 'r', encoding='utf-8') as f:
                cocktail_data = json.load(f)


            # 카테고리 필터링
            filtered_cocktails = []
            if category.lower() in ['rum', 'vodka', 'gin', 'whiskey', 'tequila', 'liqueur']:
                filtered_cocktails = [
                    {'name': name, **details}
                    for cocktail in cocktail_data
                    for name, details in cocktail.items()
                    if details.get('base_liquor', '').lower() == category.lower()
                ]
            elif category.lower() in ['low', 'middle', 'high']:
                filtered_cocktails = [
                    {'name': name, **details}
                    for cocktail in cocktail_data
                    for name, details in cocktail.items()
                    if details.get('alcohol_strength', '').lower() == category.lower()
                ]
            elif category.lower() in ['shaking', 'stir', 'build']:
                filtered_cocktails = [
                    {'name': name, **details}
                    for cocktail in cocktail_data
                    for name, details in cocktail.items()
                    if details.get('technique', '').lower() == category.lower()
                ]

            print(f"Filtered cocktails count: {len(filtered_cocktails)}")  # 디버깅 로그

            # 필터링된 데이터가 없을 때 처리
            if len(filtered_cocktails) == 0:
                return JsonResponse({'error': '선택한 카테고리에 해당하는 칵테일이 없습니다.'}, status=404)

            # 7개의 랜덤 칵테일 추출
            recommended_cocktails = random.sample(filtered_cocktails, min(7, len(filtered_cocktails)))

            # JSON 형식으로 데이터 반환
            return JsonResponse({'cocktails': recommended_cocktails})

        except Exception as e:
            # traceback을 이용한 자세한 에러 로그 출력
            error_message = traceback.format_exc()
            print(f"Error occurred: {error_message}")  # 터미널에 에러 출력
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)
    
def save_preferences(request):
    if request.method == 'POST':
        base_liquor = request.POST.getlist('base_liquor')
        alcohol_strength = request.POST.getlist('alcohol_strength')
        glass = request.POST.getlist('glass')
        technique = request.POST.getlist('technique')

        # 사용자의 프로필을 가져와 데이터를 저장
        profile = UserProfile.objects.get(user=request.user)
        profile.base_liquor = base_liquor
        profile.alcohol_strength = alcohol_strength
        profile.glass = glass
        profile.technique = technique
        profile.save()

        return redirect('my_page')
    


def recommend_personalized_cocktails(request):
    try:
        # JSON 파일 경로 설정
        json_file_path = os.path.join(settings.BASE_DIR, 'cocktail_data.json')

        # JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cocktail_data = json.load(f)

        # 로그인 상태에 따른 칵테일 필터링
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            print(f"User Profile: {profile.base_liquor}, {profile.alcohol_strength}, {profile.glass}, {profile.technique}")

            # 선택된 선호도를 기준으로 칵테일 필터링
            filtered_cocktails = [
                {'name': name, **details}
                for cocktail in cocktail_data
                for name, details in cocktail.items()
                if (not profile.base_liquor or any(base in details.get('base_liquor', '') for base in profile.base_liquor)) and
                   (not profile.alcohol_strength or any(strength in details.get('alcohol_strength', '') for strength in profile.alcohol_strength)) and
                   (not profile.glass or any(glass in details.get('glass', '') for glass in profile.glass)) and
                   (not profile.technique or any(tech in details.get('technique', '') for tech in profile.technique))
            ]
        else:
            # 로그인하지 않은 경우 전체 칵테일에서 무작위로 10개 선택
            filtered_cocktails = [
                {'name': name, **details}
                for cocktail in cocktail_data
                for name, details in cocktail.items()
            ]

        # 필터링 결과가 없는 경우 기본적으로 무작위 칵테일 10개 추천
        if not filtered_cocktails:
            filtered_cocktails = [
                {'name': name, **details}
                for cocktail in cocktail_data
                for name, details in cocktail.items()
            ]
        
        # 필터링된 칵테일 개수에 따라 10개 이하일 경우 해당 개수만큼 출력, 그 이상이면 10개 출력
        recommended_cocktails = random.sample(filtered_cocktails, min(10, len(filtered_cocktails)))

        # JSON 응답 반환
        return JsonResponse({'cocktails': recommended_cocktails})

    except Exception as e:
        print('Error:', e)  # 에러 로그 출력
        return JsonResponse({'error': str(e)}, status=500)
