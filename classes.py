import random
import time
import tkinter as tk
from threading import Thread


class SmartDevice:
    def __init__(self, id):
        self.id = id
        self.status = False

    def toggle_status(self):
        self.status = not self.status


class SmartLight(SmartDevice):
    def __init__(self, id):
        super().__init__(id)
        self.brightness = 0

    def set_brightness(self, brightness):
        self.brightness = brightness


class Thermostat(SmartDevice):
    def __init__(self, id):
        super().__init__(id)
        self.temperature = 10

    def set_temperature(self, temperature):
        self.temperature = temperature


class SecurityCamera(SmartDevice):
    def __init__(self, id):
        super().__init__(id)
        self.motion = False

    def detect_motion(self):
        self.motion = random.choice((True, False))


class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def enable(self, devices):
        if self.condition(devices):
            self.action(devices)


class AutoSystem:
    def __init__(self):
        self.devices = []
        self.rules = []

    def add_device(self, device):
        self.devices.append(device)

    def add_rule(self, rule):
        self.rules.append(rule)

    def enable_rules(self):
        for rule in self.rules:
            rule.enable(self.devices)


class Dashboard:
    def __init__(self, root, system):
        self.root = root
        self.system = system

        self.root.title("Smart Home IoT Simulator")
        self.labels = []

        self.auto_text = tk.StringVar()
        self.auto_on = True

        self.listbox = tk.Listbox(self.root, width=55)
        self.listbox.pack()

        self.create_device_interface()
        self.create_rule_interface()

        self.update_listbox()
        self.update_thread = Thread(target=self.loop)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.toggle_auto = tk.Button(self.root, text="Toggle Automation", command=self.toggle_auto)
        self.toggle_auto.pack()

        self.auto_label = tk.Label(self.root, text="Automation: On")
        self.auto_label.pack()

        self.exit_button = tk.Button(self.root, text="Exit application", command=self.root.quit)
        self.exit_button.pack()

    def toggle_auto(self):
        self.auto_on = not self.auto_on

        if self.auto_on:
            temp = "On"
        else:
            temp = "Off"

        self.auto_label.config(text=f"Automation: {temp}")

    @staticmethod
    def set_brightness(light, brightness):
        light.set_brightness(int(brightness))

    @staticmethod
    def set_temperature(thermostat, temperature):
        thermostat.set_temperature(int(temperature))

    @staticmethod
    def detect_motion(camera):
        camera.detect_motion()

    @staticmethod
    def status_toggler(device):
        device.toggle_status()

    def label_setter(self, device):
        text = tk.StringVar()

        label = tk.Label(self.root, textvariable=text)
        self.labels.append({'id': device.id, 'label': text, 'device': device})

        tk.Button(self.root, text="Toggle ON/OFF", command=lambda x=device: self.status_toggler(x)).pack()
        label.pack()

    def create_device_interface(self):
        for device in self.system.devices:
            if isinstance(device, SmartLight):
                self.create_light_interface(device)
                self.label_setter(device)

            elif isinstance(device, Thermostat):
                self.create_thermostat_interface(device)
                self.label_setter(device)

            elif isinstance(device, SecurityCamera):
                self.create_camera_interface(device)
                self.label_setter(device)

    def create_light_interface(self, light):
        label = tk.Label(self.root, text=f"{light.id} Brightness")
        label.pack()
        brightness_slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal",
                                     command=lambda v, x=light: self.set_brightness(x, v))
        brightness_slider.pack()

    def create_thermostat_interface(self, thermostat):
        label = tk.Label(self.root, text=f"{thermostat.id} temperature")
        label.pack()
        temperature_slider = tk.Scale(self.root, from_=10, to=30, orient="horizontal",
                                      command=lambda v, x=thermostat: self.set_temperature(x, v))
        temperature_slider.pack()

    def create_camera_interface(self, camera):
        label = tk.Label(self.root, text=f"{camera.id} Motion Detection")
        label.pack()
        motion_button = tk.Button(self.root, text="Random Detect Motion",
                                  command=lambda x=camera: self.detect_motion(x))
        motion_button.pack()

    def create_auto_rule(self):
        def motion(devices):
            for device in devices:
                if isinstance(device, SecurityCamera) and device.motion:
                    return True
            return False

        def turn_on_lights(devices):
            for device in devices:
                if isinstance(device, SmartLight):
                    device.status = True

        def turn_off_lights(devices):
            for device in devices:
                if isinstance(device, SmartLight):
                    device.status = False

        rule_on = Rule(motion, turn_on_lights)
        rule_off = Rule(lambda devices: not motion(devices), turn_off_lights)

        self.system.add_rule(rule_on)
        self.system.add_rule(rule_off)

    def create_rule_interface(self):
        rule_label = tk.Label(self.root, text="Automation Rule: Turn on lights when motion is detected")
        rule_label.pack()

        auto_status_label = tk.Label(self.root, textvariable=self.auto_text)
        auto_status_label.pack()

        auto_button = tk.Button(self.root, text="Create Automation Rule", command=self.create_auto_rule)
        auto_button.pack()

    def update_interface(self):
        for label in self.labels:
            device = label['device']

            if isinstance(device, SmartLight):
                label['label'].set(f"{device.id} - {f'{device.brightness}%' if device.status else '(OFF)'}")

            elif isinstance(device, Thermostat):
                label['label'].set(f"{device.id} - {f'{device.temperature}C' if device.status else '(OFF)'}")

            elif isinstance(device, SecurityCamera):
                label['label'].set(
                    f"{device.id} - Motion: {'(OFF)' if not device.status else ('YES' if device.motion else 'NO')}")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for device in self.system.devices:
            self.listbox.insert(tk.END,
                                f"{device.id}: {type(device).__name__} Status: {'On' if device.status else 'Off'}")

    def loop(self):
        while True:
            if self.auto_on:
                self.system.enable_rules()
                randomise(self.system.devices)

            self.update_interface()
            self.update_listbox()

            light_status = 'On' if any(
                isinstance(device, SmartLight) and device.status for device in self.system.devices) else 'Off'
            self.auto_text.set(f"Automation: Lights are {light_status}")

            time.sleep(0.5)


def randomise(self):
    for device in self:
        if not device.status:
            continue

        if isinstance(device, SmartLight):
            device.set_brightness(random.randint(0, 100))
        elif isinstance(device, Thermostat):
            device.set_temperature(random.randint(10, 30))
        elif isinstance(device, SecurityCamera):
            device.detect_motion()
