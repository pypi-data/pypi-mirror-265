##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.8                                                             #
# Generated on 2024-03-29T12:37:59.276388                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowGSPackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

