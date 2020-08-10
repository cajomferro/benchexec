# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Utilities for adapting older tool-info modules to the currently expected API."""

import inspect

from benchexec.tools.template import BaseTool, BaseTool2


CURRENT_BASETOOL = BaseTool2
"""Alias for the latest base-tool class in benchexec.tools.template"""


# We do not let Tool1To2 actually inherit from BaseTool2 because we do not want to
# inherit any default implementations, but we still declare it as a subclass.
@BaseTool2.register
class Tool1To2(object):
    """
    Adapter for making subclasses of BaseTool confirm to the API of BaseTool2
    """

    _FORWARDED_METHODS = [
        "executable",
        "program_files",
        "version",
        "name",
        "cmdline",
        "determine_result",
        "get_value_from_output",
        "working_directory",
        "environment",
    ]

    def __init__(self, wrapped):
        for method in Tool1To2._FORWARDED_METHODS:
            # This binds wrapped to the first argument of the method
            # such that when the method is called it can properly access its instance.
            assert not hasattr(self, method)
            setattr(self, method, getattr(wrapped, method))

        self.__doc__ = inspect.getdoc(wrapped)


def adapt_to_current_version(tool):
    """
    Given an instance of a tool-info module's class, return an instance that conforms to
    the current API. Might be either the same or a different instance.
    """
    if isinstance(tool, BaseTool2):
        return tool
    elif isinstance(tool, BaseTool):
        return Tool1To2(tool)
    else:
        raise TypeError(
            "{} is not a subclass of one of the expected base classes "
            "in benchexec.tools.template".format(tool.__class__)
        )