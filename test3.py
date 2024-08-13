from classes import *


system = AutoSystem()
system.add_device(Thermostat("Bedroom Thermostat"))
system.add_device(Thermostat("Living Room Thermostat"))
system.add_device(SecurityCamera("Front Door Camera"))

root = tk.Tk()
dashboard = Dashboard(root, system)

root.mainloop()
