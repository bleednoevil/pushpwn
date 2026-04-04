import mido
import threading
import time
import random

# =========================
# CONFIG
# =========================

MIDI_INPUT_NAME = None   # set to your device name or leave None for auto
MIDI_OUTPUT_NAME = None  # set to your device name or leave None for auto

COLOR_IDLE = 0
COLOR_ACTIVE = 60
COLOR_ALERT = 127


# =========================
# MIDI SETUP
# =========================

def get_port(name, ports):
    if name:
        for p in ports:
            if name in p:
                return p
        raise Exception(f"Port '{name}' not found")
    else:
        return ports[0]


inport = mido.open_input(get_port(MIDI_INPUT_NAME, mido.get_input_names()))
outport = mido.open_output(get_port(MIDI_OUTPUT_NAME, mido.get_output_names()))

print(f"[+] MIDI Input: {inport.name}")
print(f"[+] MIDI Output: {outport.name}")


def set_pad_color(note, velocity):
    msg = mido.Message('note_on', note=note, velocity=velocity)
    outport.send(msg)


# =========================
# EVENT BUS
# =========================

class EventBus:
    listeners = {}

    @classmethod
    def on(cls, event, callback):
        cls.listeners.setdefault(event, []).append(callback)

    @classmethod
    def emit(cls, event, *args):
        for cb in cls.listeners.get(event, []):
            cb(*args)


# =========================
# AGENT
# =========================

class ReconAgent:
    def __init__(self, pad_id, task):
        self.pad_id = pad_id
        self.task = task
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        print(f"[+] Agent {self.pad_id} started")

    def stop(self):
        self.running = False
        print(f"[-] Agent {self.pad_id} stopped")

    def run(self):
        while self.running:
            result = self.task()
            if result:
                EventBus.emit("alert", self.pad_id, result)
            time.sleep(2)


# =========================
# TASK (REPLACE THIS LATER)
# =========================

def fake_recon_task():
    # Simulated detection
    if random.randint(0, 10) > 8:
        return "Potential exposure detected"
    return None


# =========================
# AGENT MANAGEMENT
# =========================

agents = {}

def get_agent(pad_id):
    if pad_id not in agents:
        agents[pad_id] = ReconAgent(pad_id, fake_recon_task)
    return agents[pad_id]


# =========================
# EVENTS → LED FEEDBACK
# =========================

def on_alert(pad_id, result):
    print(f"[ALERT] Pad {pad_id}: {result}")
    set_pad_color(pad_id, COLOR_ALERT)

EventBus.on("alert", on_alert)


# =========================
# INPUT HANDLER
# =========================

def handle_pad_press(note, velocity):
    if velocity == 0:
        return  # ignore note_off

    agent = get_agent(note)

    if not agent.running:
        agent.start()
        set_pad_color(note, COLOR_ACTIVE)
    else:
        agent.stop()
        set_pad_color(note, COLOR_IDLE)


# =========================
# MAIN LOOP
# =========================

print("[*] PushPwn running... Press pads to toggle agents.")

try:
    for msg in inport:
        if msg.type == 'note_on':
            handle_pad_press(msg.note, msg.velocity)

except KeyboardInterrupt:
    print("\n[!] Exiting...")
    for a in agents.values():
        a.stop()
