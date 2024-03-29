#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 16:15
@Author  : alexanderwu
@File    : singleton.py
"""
import abc


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
