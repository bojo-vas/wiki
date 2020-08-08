from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms

import markdown2
from random import choice

from . import util


class SearchForm(forms.Form):
    searched = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}), max_length=100)


def index(request):
    form = SearchForm()
    context = {
        "header": "All Pages",
        "entries": util.list_entries(),
        "form": form
    }
    return render(request, "encyclopedia/index.html", context)


def error(request):
    context = {
        "title": "Error",
        "text": ["<H1>Error</H1>", "<p>Requested page was not found</p>"],
        "form": SearchForm()
    }
    return render(request, "encyclopedia/topic.html", context)


def random(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("topic", args=[choice(entries), ]))


def topic(request, title):
    found = util.get_entry(title)
    if found:
        text = markdown2.markdown(found)

        context = {
            "title": title,
            "text": [i for i in text.split('\n')],
            "form": SearchForm()
        }

        return render(request, "encyclopedia/topic.html", context)
    return HttpResponseRedirect(reverse("error"))


def search(request):
    results = []
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["searched"].lower()
            entries = util.list_entries()
            for title in entries:
                if text in title.lower():
                    results.append(title)

    else:
        form = SearchForm()

    context = {
        "header": "Found Results",
        "entries": results,
        "form": form
    }
    return render(request, "encyclopedia/index.html", context)

