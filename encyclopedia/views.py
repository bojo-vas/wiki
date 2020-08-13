from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import markdown2
from random import choice

from . import util, forms


def index(request):
    form = forms.SearchForm()
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
        "form": forms.SearchForm(),
        "error": True
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
            "form": forms.SearchForm()
        }
        request.session["last_entry"] = found

        return render(request, "encyclopedia/topic.html", context)

    return HttpResponseRedirect(reverse("error"))


def search(request):
    results = []
    if request.method == "POST":
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["searched"].lower()
            entries = util.list_entries()
            for title in entries:
                if text == title.lower():
                    return HttpResponseRedirect(reverse("topic", args=[text, ]))
                elif text in title.lower():
                    results.append(title)

    else:
        form = forms.SearchForm()

    context = {
        "header": "Found Results",
        "entries": results,
        "form": form
    }
    return render(request, "encyclopedia/index.html", context)


def new_page(request):
    duplicated = False
    title = None
    content = None

    if request.method == "POST":
        add_form = forms.NewPage(request.POST)

        if add_form.is_valid():
            title = add_form.cleaned_data["title"]
            while not title[0].isalnum():
                title = title[1:]

            content = add_form.cleaned_data["content"]
            entries = util.list_entries()

            if title.lower() in [entry.lower() for entry in entries] and not request.session["edit_mode"]:
                duplicated = True

            else:
                if not title.isupper():
                    title = title.title()
                full_content = f"# {title}\n\n{content}"
                util.save_entry(title, full_content)
                return HttpResponseRedirect(reverse("topic", args=[title, ]))

    else:
        add_form = forms.NewPage()

    context = {
        "header": "New Entry",
        "form": forms.SearchForm(),
        "add_form": add_form.as_p(),
        "duplicated": duplicated,
        "title": title,
        "content": content,
    }
    return render(request, "encyclopedia/new_page.html", context)


def edit_page(request):
    request.session["edit_mode"] = True
    last_page = request.session["last_entry"].split("\n")
    full_content = [line for line in last_page if line.strip() != '']

    title = full_content[0].strip("#").lstrip()
    content = '\n'.join(full_content[1:]).lstrip()

    add_form = forms.NewPage(initial={'title': title, 'content': content})

    context = {
        "header": "Edit Entry",
        "form": forms.SearchForm(),
        "add_form": add_form.as_p(),
        "duplicated": False,
        "title": title,
        "content": content,
    }

    return render(request, "encyclopedia/new_page.html", context)