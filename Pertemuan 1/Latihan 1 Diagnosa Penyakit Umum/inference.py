import collections
import collections.abc
# Kompatibilitas Python 3.10+
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import PenyakitRules


class DiagnosaPenyakit(KnowledgeEngine, PenyakitRules):
    """Mesin inferensi diagnosa penyakit umum"""
    pass
