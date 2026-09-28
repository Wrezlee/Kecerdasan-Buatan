import collections
import collections.abc
# Kompatibilitas Python 3.10+
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import MentalRules


class DiagnosaMental(KnowledgeEngine, MentalRules):
    """Mesin inferensi diagnosa kondisi mental"""
    pass
