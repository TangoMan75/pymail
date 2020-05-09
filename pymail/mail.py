#!/bin/python3
# -*- coding: utf-8 -*-

"""
 This file is part of the TangoMan PyMail package.

 (c) "Matthias Morin" <mat@tangoman.io>

 This source file is subject to the MIT license that is bundled
 with this source code in the file LICENSE.
"""

from base64 import b64decode
from datetime import datetime
from email import (message_from_file, message_from_string)
from email.header import decode_header
from email.message import Message
from email.utils import parseaddr
from quopri import decodestring
from re import sub
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup as soup


class Email:
    """
    Parse eml files
    https://docs.python.org/3/library/email.parser.html
    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    """

    ##################################################

    def __init__(self, path: str = None) -> None:
        self._path = None
        self._raw = None
        self._message = None
        if path is not None:
            self.read(path)

    ##################################################

    @property
    def path(self) -> Optional[str]:
        """Get file path"""
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """Set file path"""
        if not isinstance(path, str):
            raise TypeError('{}.path must be set to a string, {} given'.format(self.__class__.__name__, type(path)))
        if not path:
            raise ValueError('{}.path file_path cannot be empty'.format(self.__class__.__name__))
        self._path = path

    ##################################################

    def read(self, path: str) -> None:
        """Get email message from file"""
        self.path = path
        try:
            with open(self._path, 'r', encoding='utf-8', newline='') as file:
                self._raw = message_from_file(file)
        except Exception as e:
            raise e

    ##################################################

    @property
    def raw(self) -> Optional[Message]:
        """Get raw message"""
        return self._raw

    @raw.setter
    def raw(self, message: str) -> None:
        """Set raw message from string"""
        if not isinstance(message, str):
            raise TypeError(
                '{}.message must be set to a string, {} given'.format(self.__class__.__name__, type(message)))
        if not message:
            raise ValueError('{}.message file_path cannot be empty'.format(self.__class__.__name__))
        self._raw = message_from_string(message)

    ##################################################

    @property
    def message(self) -> Optional[str]:
        """Get message body"""
        message = ''
        if self._raw.is_multipart():
            for payload in self._raw.get_payload():
                message += payload.get_payload()
        else:
            message = self._raw.get_payload()
        # decode base64 encoded message
        if self._raw['Content-Transfer-Encoding'] == 'base64':
            message = b64decode(message)
        # decode MIME quoted-printable data
        return decodestring(message)

    ##################################################

    @property
    def datetime(self) -> Optional[datetime]:
        """"Get datetime"""
        if self._raw is not None:
            sanitized_date = sub(' [+-].+$', '', self._raw['Date'])
            return datetime.strptime(sanitized_date, '%a, %d %b %Y %H:%M:%S')
        return None

    ##################################################

    @property
    def date(self) -> Optional[str]:
        """"Get date"""
        if self._raw is not None:
            return str(self.datetime.date())
        return None

    ##################################################

    @property
    def time(self) -> Optional[str]:
        """"Get time"""
        if self._raw is not None:
            return str(self.datetime.time()).replace(':', '-')
        return None

    ##################################################

    @property
    def subject(self) -> Optional[str]:
        """Get subject"""
        if self._raw is not None:
            # decode_header handles encoded string e.g: "=?UTF-8?B?XXXXXXXXXX=?="
            result = decode_header(self._raw['Subject'])[0][0]
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            return result
        return None

    ##################################################

    @property
    def sender_name(self) -> Optional[str]:
        """Get sender_name"""
        if self._raw is not None:
            from_ = decode_header(self._raw['From'])[0][0]
            if isinstance(from_, bytes):
                from_ = from_.decode('utf-8')
            return parseaddr(from_)[0]
        return None

    ##################################################

    @property
    def sender_email(self) -> Optional[str]:
        """Get sender_email"""
        if self._raw is not None:
            from_ = decode_header(self._raw['From'])[0][0]
            if isinstance(from_, bytes):
                from_ = from_.decode('utf-8')
            return parseaddr(from_)[1]
        return None

    ##################################################

    @property
    def return_path(self) -> Optional[str]:
        """Get return_path"""
        if self._raw is not None:
            result = decode_header(self._raw['Return-Path'])[0][0]
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            return parseaddr(result)[1]
        return None

    ##################################################

    @property
    def urls(self) -> list:
        """Return all urls from message body"""
        try:
            page_soup = soup(self.message, 'html.parser')
            links = page_soup.find_all('a', href=True)
            images = page_soup.find_all('img', src=True)
        except Exception as e:
            raise e
        urls = []
        for item in links:
            href = item['href']
            if href != '':
                urls.append(href)
        for item in images:
            src = item['src']
            if src != '':
                urls.append(src)
        return sorted(set(urls))

    ##################################################

    @property
    def hostnames(self) -> list:
        """Return all hostnames from message"""
        hostnames = []
        for link in self.urls:
            temp = urlparse(link).netloc
            if temp != '':
                hostnames.append(temp)
        for address in (self.sender_email, self.return_path):
            temp = address.split('@')
            if len(temp) == 2:
                hostnames.append(temp[1])
        return sorted(set(hostnames))

    ##################################################


if __name__ == '__main__':
    pass
