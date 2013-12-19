#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, RequestContext
import urllib2
import json
from utils import UrlDoc

URL_DOC = "http://localhost:5000/api/v1/doc"


def home(request):
    return render_to_response('general/home.html', {}, RequestContext(request))


def api_doc(request):
    headers = {"Accept": "application/json"}
    req = urllib2.Request(URL_DOC, headers=headers)
    response = urllib2.urlopen(req)
    doc_json = json.loads(response.read())
    list_urls = []
    for url in doc_json:
        list_urls.append(UrlDoc(url, doc_json[url]['doc'], doc_json[url]['methods'], doc_json[url]['consumes'],
                                doc_json[url]['produces']))

    c = {
        'urls': list_urls,
    }
    return render_to_response('general/documentation.html', c, RequestContext(request))
