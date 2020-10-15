# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


""" docstring """

import hashlib

# object encode / decode

class ObjectCodec():
    """ docstring """

    @staticmethod
    def encode(arg_object):
        """ docstring """
        return arg_object.encode('utf-8')

    @staticmethod
    def decode(arg_object):
        """ docstring """
        return arg_object.decode('utf-8')

# hashing

class Hashing():
    """ docstring """

    @staticmethod
    def hash_sha1(arg_object):
        """ docstring """
        return hashlib.sha1(arg_object).hexdigest()

    @staticmethod
    def integer_hash(arg_hex_digest):
        """ docstring """
        return int(arg_hex_digest[:8], 16) # 8 hex digits of precision

# END ##########################################################################
