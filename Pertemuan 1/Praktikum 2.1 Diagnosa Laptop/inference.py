import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import LaptopRules

class DiagnosaLaptop(KnowledgeEngine,
                     LaptopRules):
    """Inference Engine"""
    pass