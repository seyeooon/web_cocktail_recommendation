import json
from django.shortcuts import render
import re  # 정규 표현식을 사용하기 위한 import
import requests
import base64
import time, os
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.models import User


# 전역 변수로 토큰과 만료 시간 저장
SPOTIFY_TOKEN = None
TOKEN_EXPIRES_AT = None

def cocktail_detail(request, cocktail_name):
    if request.method == 'POST':
        # JSON 파일에서 칵테일 데이터를 불러오기
        with open('cocktail_data.json', 'r', encoding='utf-8') as f:
            cocktail_data = json.load(f)
        
        # 칵테일 이름을 리스트에서 검색
        cocktail_info = None
        for cocktail in cocktail_data:
            if cocktail_name in cocktail:
                cocktail_info = cocktail[cocktail_name]
                break
        
        if not cocktail_info:
            return render(request, 'cocktail/not_found.html', {'cocktail_name': cocktail_name})

        # Ingredients를 쉼표로 나눠서 리스트로 변환 후, 각 항목을 "ingredient - amount"로 변환
        if 'ingredients' in cocktail_info:
            ingredients_list = cocktail_info['ingredients'].split(',')
            formatted_ingredients = []
            for ingredient in ingredients_list:
                # 괄호 기준으로 split
                parts = ingredient.split('(')
                if len(parts) == 2:
                    formatted_ingredient = f"{parts[0].strip()} - {parts[1].strip(')')}"
                else:
                    formatted_ingredient = ingredient.strip()  # 괄호가 없을 경우 그대로 사용
                formatted_ingredients.append(formatted_ingredient)
            cocktail_info['ingredients'] = formatted_ingredients
        
         # Recipe가 존재하는 경우 정규식을 사용하여 숫자가 아닌 점(.)만을 기준으로 나눔
        if 'recipe' in cocktail_info and cocktail_info['recipe']:
            # 정규 표현식: 숫자와 상관없는 점을 기준으로 나누기
            recipe_steps = re.split(r'(?<!\d)\.\s*', cocktail_info['recipe'])
            cocktail_info['recipe'] = [step.strip() for step in recipe_steps if step.strip()]
        
        # Spotify API를 사용해 음악 추천 받기
        spotify_client_id = 'YOUR_SPOTIFY_CLIENT_ID'
        spotify_client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'
        token = get_spotify_token(spotify_client_id, spotify_client_secret)
        music_recommendations = get_music_recommendations(cocktail_name, token)
        
        # 칵테일 이름을 함께 전달
        return render(request, 'cocktail/cocktail_detail.html', {
            'cocktail': cocktail_info, 
            'cocktail_name': cocktail_name, 
            'music_recommendations': music_recommendations  # 음악 추천 리스트를 템플릿에 전달
        })
    
    return render(request, 'cocktail/not_found.html', {'error': 'Invalid request method'})


def get_spotify_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'27209bbf727f497f9cf8b2a95b43ca4c:e3f76c5caa6b4a7ab1f21294bd70cb2b'.encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get('access_token')
    return token

def get_music_recommendations(cocktail_name, token):
    url = f'https://api.spotify.com/v1/search?q={cocktail_name}&type=track&limit=3'  # 칵테일 이름을 검색
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        tracks = response.json()['tracks']['items']
        music_recommendations = []
        for track in tracks:
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            track_url = track['external_urls']['spotify']
            music_recommendations.append({
                'track_name': track_name,
                'artist_name': artist_name,
                'track_url': track_url
            })
        return music_recommendations
    else:
        return None
