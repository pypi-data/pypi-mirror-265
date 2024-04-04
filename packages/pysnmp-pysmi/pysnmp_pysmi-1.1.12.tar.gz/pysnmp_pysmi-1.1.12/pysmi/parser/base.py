#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysmi/license.html
#


class AbstractParser:
    def reset(self):
        raise NotImplementedError()

    def parse(self, data, **kwargs):
        raise NotImplementedError()
