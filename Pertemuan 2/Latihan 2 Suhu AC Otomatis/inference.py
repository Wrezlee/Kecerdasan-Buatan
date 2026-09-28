from skfuzzy import control as ctrl
from rules import rules

# =====================================
# MEMBANGUN SISTEM FUZZY
# =====================================

sistem = ctrl.ControlSystem(rules)
ac = ctrl.ControlSystemSimulation(sistem)
