#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC


class PackageSupportConfig(ABC):
    @staticmethod
    def isEnabled() -> bool: ...
    @staticmethod
    def enable() -> None: ...
    @staticmethod
    def disable() -> None: ...
