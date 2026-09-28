import collections
import collections.abc
# Kompatibilitas Python 3.10+
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import PadiRules


class DiagnosaPadi(KnowledgeEngine, PadiRules):
    """Mesin inferensi"""
    pass
