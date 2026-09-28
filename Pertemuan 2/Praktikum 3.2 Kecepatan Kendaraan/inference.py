from skfuzzy import control as ctrl
from rules import rules

# =====================================
# MEMBANGUN SISTEM FUZZY
# =====================================

speed_ctrl = ctrl.ControlSystem(rules)
speed = ctrl.ControlSystemSimulation(speed_ctrl)
