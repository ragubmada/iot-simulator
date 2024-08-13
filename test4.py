from classes import *


system = AutoSystem()
system.add_device(SmartLight("Light 1"))
system.add_device(SmartLight("Light 2"))
system.add_device(SmartLight("Light 3"))
system.add_device(Thermostat("Living Room Thermostat"))

root = tk.Tk()
dashboard = Dashboard(root, system)

root.mainloop()
