# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from system import System


if __name__ == '__main__':
    system = System(1000)
    system.start()
    system.stats()
