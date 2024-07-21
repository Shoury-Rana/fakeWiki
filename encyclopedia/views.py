from django import forms
from django.shortcuts import render
from django.urls import reverse
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from random import randint

class searchform(forms.Form):
    query = forms.CharField(label='search')

class create(forms.Form):
    title = forms.CharField(label='title')
    content = forms.CharField(label='content', widget=forms.Textarea())

class changes(forms.Form):
    content = forms.CharField(label='content', widget=forms.Textarea())


def index(request):
    pages = util.list_entries
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'search': searchform(),
        'pages': pages
    })

def page(request, title):
    get_page = util.get_entry(title)
    form = searchform()
    if get_page == None:
        l = []
        entries = util.list_entries()
        for i in entries:
            if title.lower() in i.lower():
                l.append(i)
        return render(request, 'encyclopedia/suggest.html', {
            'searched': title,
            'search': form,
            'list': l
        })
    
    return render(request, 'encyclopedia/page.html', {
        'title': title,
        'page': get_page,
        'search': form
    })

def search(request):
    if request.method == 'POST':
        form = searchform(request.POST)
        if form.is_valid():
            q = form.cleaned_data['query']
            return HttpResponseRedirect(reverse('encyclopedia:page', kwargs={'title': q}))

def createPage(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/create.html', {
            'search': searchform(),
            'form': create()
        })
    else:
        form = create(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title in util.list_entries():
                return HttpResponse(f'Error, file with title "{title}" already exist.')
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        
def edit(request, title):
    if request.method == 'POST':
        form = changes(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:page', kwargs={'title': title}))

    get_page = util.get_entry(title)
    form = searchform()
    change = changes(initial={'content': get_page})
    return render(request, 'encyclopedia/confirmation.html', {
        'title': title,
        'search': form,
        'changes': change
    })

def random(request):
    list = util.list_entries()
    index = randint(0, len(list)-1)
    return HttpResponseRedirect(reverse('encyclopedia:page', kwargs={'title': list[index] }))


                