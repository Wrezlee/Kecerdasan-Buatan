from skfuzzy import control as ctrl
from rules import rules

# =====================================
# MEMBANGUN SISTEM FUZZY
# =====================================

sistem = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(sistem)
