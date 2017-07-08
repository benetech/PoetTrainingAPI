# -*- coding: utf-8 -*-
"""A file for all locales and string constants."""


class Errors:
    """A class to contain all the error constants."""

    BAD_GUID = ('bad-guid', 'We couldn\'t understand the format of the ID.')
    USER_NOT_FOUND = ('user-not-found', 'We couldn\'t find that user')
    RESOURCE_NOT_FOUND = ('resource-not-found',
                          'We couldn\'t find that resource')
    FILE_NOT_SENT = ('file-not-sent', 'No file was sent.')
    FILE_NAME_REQUIRED = ('file-name-required', 'A submitted file must have a '
                                                'name.')
    IMAGE_TYPE_NOT_SUPPORTED = ('image-type-not-supported',
                                'We don\'t allow images with that extension')
    FILE_EMPTY = ('file-required', 'An empty file was sent.')
    UNKNOWN_ERROR = ('unknown-error', 'An unknown error occurred. Contact an '
                                      'administrator if the problem persists.')
