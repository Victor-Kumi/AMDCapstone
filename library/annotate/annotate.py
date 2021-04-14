# MIT LINCENCE. 2021
#
# This file is part of an academic capstone project,
# and it is made for AMD as part of efforts to automate
# the open source ROCM math libraries performance analytics.
# Contact The AMD rocm team for use and improvements on the project.
# The team: Victor Tuah Kumi, Aidan Forester, Javier Vite, Ahmed Iqbal
# Reach Victor Tuah Kumi on LinkedIn

"""Annotation factory for method arguments in library"""
from typing import Annotated
from typing import Union

class AnnotationFactory:
    """Annotate the arg variables"""
    def __init__(self, type_hint):
        self.type_hint = type_hint

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return Annotated[(self.type_hint, ) + key]
        else:
            return Annotated[self.type_hint, key]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type_hint})"

STRING_HINT =  Union[AnnotationFactory(str), None]
STRING = STRING_HINT['hardware id or rocm version, None']
PATH =  AnnotationFactory(str)
PATH = PATH['path']
PATH_LIST = AnnotationFactory(list)
DAT_FILE_PATH_HINT = Union[PATH, PATH_LIST[PATH], None]
DAT_FILE_PATH = DAT_FILE_PATH_HINT['path, paths, None']
STRING_LIST = AnnotationFactory(list)
STRING_LIST = PATH_LIST['string']
DICT = AnnotationFactory(dict)
DICT = DICT['key: string, value: list']
