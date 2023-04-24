import random
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.http import Http404
from django.db.models import Q
import markdown

from . import util
def layout(request):
    listofentries = util.list_entries()
    random_entry = random.choice(listofentries)
    print(random_entry)
    context = {'random_entry': random_entry, 'entries': listofentries}
    return render(request, 'encyclopedia/layout.html', context)


def index(request):
    listofentries = util.list_entries()
    random_entry = random.choice(listofentries)
    print(random_entry)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 'result': False,'random_entry': random_entry
    })  
def entry(request, entry):
    markdown_text = util.get_entry(entry)
    print(markdown_text)
   
    if markdown_text is None:
        return render(request, "encyclopedia/error.html", {
            "title": entry
        })
    html = markdown.markdown(markdown_text)
    return render(request, "encyclopedia/entry.html", {
        "entry": html, "title": entry
    })
def search(request):
    my_list = util.list_entries()
    query = request.GET.get('q')
    if not query:
        return redirect('index')
    if query in my_list:
        return redirect('entry', entry=query)
    else:
        matches = [string for string in my_list if query.lower() in string.lower()]
        if matches:
            return render(request, "encyclopedia/index.html", {
            "entries": matches, 'result': True
        })
        else:
            return render(request, "encyclopedia/error.html", {
            "title": query
        })
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        try:
            if title in util.list_entries():
                raise ValidationError('Title already exists')
            util.save_entry(title, content)
        except ValidationError as e:
            return render(request, "encyclopedia/create_page.html", {
                "error_message": str(e)
            })
        return redirect('entry', entry=title)
    return render(request, "encyclopedia/create_page.html")
def edit(request, entry):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', entry=title)
    markdown_text = util.get_entry(entry)
    print(markdown_text)
    return render(request, "encyclopedia/edit_page.html", {
        "markdown_text": markdown_text, "title": entry
    })




