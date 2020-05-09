#!/bin/python3
# -*- coding: utf-8 -*-

"""
 This file is part of the TangoMan PyMail package.

 (c) "Matthias Morin" <mat@tangoman.io>

 This source file is subject to the MIT license that is bundled
 with this source code in the file LICENSE.
"""

from datetime import datetime
from email.message import Message
from os.path import dirname
from unittest import TestCase

from pymail.mail import Email


class EmailTest(TestCase):
    """
    EmailTest
    """

    def setUp(self):
        self.current_directory = dirname(__file__)
        self.email = Email(self.current_directory + '/dummy.eml')

    #################################################
    # Test Constructor
    #################################################

    def test_email_constructor_typeerror(self):
        """==> invalid type should raise TypeError"""
        with self.assertRaises(TypeError):
            Email(b'')

    def test_email_constructor_valueerror(self):
        """==> invalid value should raise ValueError"""
        with self.assertRaises(ValueError):
            Email('')

    #################################################
    # Test path setter
    #################################################

    def test_email_path_typeerror(self):
        """==> invalid type should raise TypeError"""
        with self.assertRaises(TypeError):
            self.email.path = b''

    def test_email_path_valueerror(self):
        """==> invalid value should raise ValueError"""
        with self.assertRaises(ValueError):
            self.email.path = ''

    def test_email_path(self):
        """==> path property should return expected value"""
        self.assertEqual(self.email.path, self.current_directory + '/dummy.eml')

    #################################################
    # Test raw setter
    #################################################

    def test_email_raw_typeerror(self):
        """==> invalid type should raise TypeError"""
        with self.assertRaises(TypeError):
            self.email.raw = b''

    def test_email_raw_valueerror(self):
        """==> invalid value should raise ValueError"""
        with self.assertRaises(ValueError):
            self.email.raw = ''

    def test_email_raw(self):
        """==> raw property should return expected value"""
        self.assertIsInstance(self.email.raw, Message)

    #################################################
    # Test read method
    #################################################

    def test_email_read_typeerror(self):
        """==> invalid type should raise TypeError"""
        with self.assertRaises(TypeError):
            self.email.read(b'')

    def test_email_read_valueerror(self):
        """==> invalid value should raise ValueError"""
        with self.assertRaises(ValueError):
            self.email.read('')

    #################################################
    # Test values
    #################################################

    def test_email_expected_types(self):
        """==> email should return expected type"""
        self.assertIsInstance(self.email.datetime, datetime)
        self.assertIsInstance(self.email.message, bytes)
        self.assertIsInstance(self.email.subject, str)
        self.assertIsInstance(self.email.time, str)
        self.assertIsInstance(self.email.date, str)
        self.assertIsInstance(self.email.sender_email, str)
        self.assertIsInstance(self.email.sender_name, str)
        self.assertIsInstance(self.email.return_path, str)

    def test_email_expected_values(self):
        """==> email should return expected value"""
        self.assertEqual(str(self.email.datetime), '2020-01-01 00:00:00')
        self.assertEqual(self.email.subject, 'Spam, Spam, Spam, Spam, Spam')
        self.assertEqual(self.email.time, '00-00-00')
        self.assertEqual(self.email.date, '2020-01-01')
        self.assertEqual(self.email.sender_email, 'no-reply@spammer.com')
        self.assertEqual(self.email.sender_name, 'Spammer')
        self.assertEqual(self.email.return_path, 'no-reply@spammer.com')

    def test_base64_encoded_message(self):
        """==> base64 encoded message should return expected value"""
        email = Email(self.current_directory + '/base64.eml')
        self.assertEqual(email.message, self.email.message)

    def test_extract_urls(self):
        """==> urls property should return expected value"""
        self.assertIsInstance(self.email.urls, list)
        self.assertEqual(self.email.urls, ['https://tangoman.io/image.jpg', 'https://tangoman.io/spam'])

    def test_extract_hostnames(self):
        """==> hostnames property should return expected value"""
        self.assertIsInstance(self.email.hostnames, list)
        self.assertEqual(self.email.hostnames, ['spammer.com', 'tangoman.io'])
