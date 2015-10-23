# -*- coding: utf-8 -*-
from __future__ import absolute_import

class Curl(object):

    """
    Polymorphic class that takes various request objects and translates them
    to viable curl commands.
    """
    _registry = {}

    def __init__(self, request):
        """
        Args:
            request: A "request" object from a supported library.

            Specifically one of:
                - django.http.request.HttpRequest
                - requests.models.[Response, Request, PreparedRequest]
                - urllib2.Request
        """
        self.request = request

        if self.__class__ is Curl:
            for new_class, instance_check in self._registry.items():
                if isinstance(request, instance_check):
                    if isinstance(self, Curl):
                        self.wrapper = new_class(request)
                    break
            else:
                raise TypeError('request of type {} is not of supported class type {}'.format(
                    type(request),
                    self._registry.values(),
                ))

    def __str__(self):
        return self.curl()

    @property
    def headers(self):
        return self.wrapper.headers

    @property
    def method(self):
        return self.wrapper.method

    @property
    def absolute_uri(self):
        return self.wrapper.absolute_uri

    def curl(self):
        """
        Returns(str): string that can be run as a curl command
        """
        curl = (
            'curl -X {method} \'{absolute_uri}\' {headers}'
        ).format(
            absolute_uri=self.absolute_uri,
            method=self.method,
            headers=' '.join(
                '-H \'{}: {}\''.format(name, value)
                for name, value
                in self.headers
            )
        )
        return curl

    @classmethod
    def register(cls):
        cls._registry[cls] = cls.SUPPORTED_TYPES


def curlit(request, strify=True):
    c = Curl(request)
    if strify:
        c = str(c)
    return c
