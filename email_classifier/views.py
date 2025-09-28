from django.shortcuts import render
from .nlp import process_email

def index(request):
    if request.method == "POST":
        content = request.POST.get("content")
        result = process_email(content)
        return render(request, "index.html", result)
    return render(request, "index.html")