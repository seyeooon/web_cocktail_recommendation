import json
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Comment
from django.contrib.auth.models import User
import os
from django.shortcuts import get_object_or_404


# Load the cocktail data from JSON
def load_cocktail_data():
    json_file_path = os.path.join(settings.BASE_DIR, 'cocktail_data.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        cocktail_data = json.load(file)
    return cocktail_data


# General community page
def general_community(request):
    comments = Comment.objects.filter(cocktail__isnull=True)
    return render(request, 'community/general_community.html', {'comments': comments})


# Cocktail-specific community page
def cocktail_community(request, cocktail_name):
    cocktail_data = load_cocktail_data()
    
    # 리스트에서 cocktail_name이 있는지 확인
    cocktail = None
    for item in cocktail_data:
        if cocktail_name in item:
            cocktail = item[cocktail_name]
            break

    if not cocktail:
        return redirect('general_community')  # If cocktail not found, go back to general community

    # 댓글 필터링
    comments = Comment.objects.filter(cocktail=cocktail_name)

    # cocktail_name 변수를 템플릿으로 전달
    return render(request, 'community/cocktail_community.html', {
        'cocktail': cocktail,  # 칵테일 정보를 템플릿에 전달
        'cocktail_name': cocktail_name,  # 칵테일 이름을 템플릿에 전달
        'comments': comments
    })


# Add a comment (for both general and cocktail-specific community)
def add_comment(request, cocktail_name=None):
     if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        user = request.user if request.user.is_authenticated else None
        cocktail = None

        if cocktail_name:
            cocktail = cocktail_name

        comment = Comment.objects.create(cocktail=cocktail, user=user, title=title, content=content)
        
        print(f"New comment added: {title}, {content}")  # 여기도 확인
        
        if cocktail:
            return redirect('cocktail_community', cocktail_name=cocktail_name)
        return redirect('general_community')  # 여기서 템플릿이 아닌 URL 이름으로 리다이렉션

def delete_comment(request, comment_id, cocktail_name=None):
    # comment_id로 해당 댓글을 가져옴
    comment = get_object_or_404(Comment, id=comment_id)

    # 댓글을 삭제 (작성자 확인 없이)
    comment.delete()
    print(f"Comment with ID {comment_id} deleted.")
    
    # 삭제 후 해당 칵테일 커뮤니티 페이지로 리다이렉트
    if cocktail_name:
        return redirect('cocktail_community', cocktail_name=cocktail_name)
    return redirect('general_community')
