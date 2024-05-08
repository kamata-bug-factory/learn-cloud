import base64
import os
from io import BytesIO

from app.forms import PostsForm
from app.models import Posts
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from wordcloud import WordCloud


# Create your views here.
@require_http_methods(["GET", "POST"])
def top(request):
    if request.method == "GET":
        form = PostsForm()
        posts = Posts.objects.all()
        wordcloud_image = _generate_wordcloud(posts)
        context = {
            "form": form,
            "posts": posts,
            "wordcloud_image": wordcloud_image,
        }
        return render(request, "top.html", context)

    elif request.method == "POST":
        # フォームから投稿が送信されたときの処理
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()
            # 登録された投稿を一覧に反映するため再読み込みする
            return redirect(top)


def _generate_wordcloud(posts):
    if len(posts) == 0:
        return
    skill_names = [post.skill_name for post in posts]
    text = ";".join(skill_names)
    font_path = os.path.join("app", "static", "fonts", "ipaexg00401", "ipaexg.ttf")
    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color="white",
        regexp=r"[^;]+",
        collocations=False,
    ).generate(text)
    return _to_image(wordcloud)


def _to_image(wordcloud):
    # ワードクラウドを画像に変換
    image = wordcloud.to_image()
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_png = buffer.getvalue()
    buffer.close()

    # 画像データをBase64エンコードしてバイナリ型にする
    image_base64_binary = base64.b64encode(image_png)
    # UTF-8で文字列にデコードしてHTMLに埋め込める形式にする
    image_base64_string = image_base64_binary.decode("utf-8")
    return image_base64_string
