# -*- coding: utf-8 -*-
# Copyright (c) 2020-2023 Salvador E. Tropea
# Copyright (c) 2020-2023 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
from .macros import macros, pre_class  # noqa: F401
from .error import (KiPlotConfigurationError)


@pre_class
class Ignore_Unconnected(BasePreFlight):  # noqa: F821
    """ [boolean=false] **Deprecated**, use the `ignore_unconnected` option from `run_drc`.
        Option for `run_drc`. Ignores the unconnected nets. Useful if you didn't finish the routing.
        It will also ignore KiCad 6 warnings """
    def __init__(self, name, value):
        super().__init__(name, value)
        if not isinstance(value, bool):
            raise KiPlotConfigurationError('must be boolean')
        self._enabled = value

    def get_example():
        """ Returns a YAML value for the example config """
        return 'false'

    def apply(self):
        BasePreFlight._set_option('ignore_unconnected', self._enabled)  # noqa: F821
