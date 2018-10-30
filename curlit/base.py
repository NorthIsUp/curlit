# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six


def join(strings, multiline=False):
    joiner = ' \n\t' if multiline else ' '
    return joiner.join(str(_).strip() for _ in strings if _)


class OptionsDict(dict):

    def add_option(self, option_key, *values):
        for value in values:
            if not value or value is NotImplemented:
                continue

            value = '\'{}\''.format(value)
            self.setdefault(option_key, []).append(value)

    def options(self, multiline=False):
        return join((
            '{} {}'.format('--' + option_key if option_key else option_key, value).strip()
            for option_key in self
            for value in self[option_key]
            ),
            multiline=multiline
        )
    def __str__(self):
        return self.options()


@six.python_2_unicode_compatible
class Curl(object):
    """
    Polymorphic class that takes various request objects and translates them
    to viable curl commands.
    """
    __registry__ = {}

    SUPPORTED_TYPES = ()

    def __new__(cls, request, *args, **kwargs):
        """
        Args:
            request: A "request" object from a supported library.

            Specifically one of:
                - django.http.request.HttpRequest
                - requests.models.[Response, Request, PreparedRequest]
                - urllib.Request
        """
        if cls is Curl:
            for new_class, instance_check in cls.__registry__.items():
                if isinstance(request, instance_check):
                    return super(Curl, new_class).__new__(new_class)
            else:
                raise TypeError('request of type {} is not of supported class type {}'.format(
                    type(request),
                    [_ for _ in cls.__registry__.values()],
                ))
        else:
            return super(Curl, cls).__new__(cls)

    def __init__(self, request):
        self.request = request
        self._options = OptionsDict()

    def __str__(self):
        return self.curl()

    @property
    def __headers__(self):
        '''Wrapper to make headers in the correct format'''
        for header, value in self.headers:
            yield '{}: {}'.format(header, value)

    @property
    def options(self):
        if not self._options:
            self._options.add_option('', self.absolute_uri)
            self._options.add_option('request', self.method)
            self._options.add_option('header', *self.__headers__)
            self._options.add_option('data', self.data)
        return self._options

    @property
    def headers(self):
        return NotImplemented

    @property
    def method(self):
        return NotImplemented

    @property
    def absolute_uri(self):
        return NotImplemented

    @property
    def data(self):
        return NotImplemented

    def curl(self, verbose=False, multiline=False):
        """
        Returns(str): string that can be run as a curl command
        """
        verbosity = '-' + 'v' * verbose if verbose else ''

        options = self.options.options(multiline=multiline)
        return join(('curl', verbosity, options), multiline=multiline)

    @classmethod
    def register(cls):
        cls.__registry__[cls] = cls.SUPPORTED_TYPES
