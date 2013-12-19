#!/usr/bin/env python
# -*- coding: utf-8 -*-


class UrlDoc(object):
    def __init__(self, url, doc, headers, consumes, produces):
        self.url = url
        self.doc = doc
        self.headers = headers
        self.consumes = consumes
        self.produces = produces
        self.prefix = "http://localhost:5000"

    def __unicode__(self):
        return self.url

    def get_headers(self):
        return ", ".join(self.headers)

    def get_consumes(self):
        return ", ".join(self.consumes)

    def get_produces(self):
        return ", ".join(self.produces)

    def get_status(self):
        if "GET" in self.headers:
            return '<span class="label label-primary">GET</span>'
        if "POST" in self.headers:
            return '<span class="label label-success">POST</span>'
        if "PUT" in self.headers:
            return '<span class="label label-warning">PUT</span>'
        if "DELETE" in self.headers:
            return '<span class="label label-danger">DELETE</span>'
        return '<span class="label label-success">GET</span>'
