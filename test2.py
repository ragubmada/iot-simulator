from classes import *


system = AutoSystem()
system.add_device(SmartLight("Light 1"))
system.add_device(SmartLight("Light 2"))
system.add_device(SmartLight("Light 3"))
system.add_device(SmartLight("Light 4"))
system.add_device(SmartLight("Light 5"))
system.add_device(SecurityCamera("Front Door Camera"))

root = tk.Tk()
dashboard = Dashboard(root, system)

root.mainloop()
