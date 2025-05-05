import tkinter as tk
from tkinter import messagebox
import time
import threading

class TuringMachine:
    def __init__(self, tape, transitions, head_position=0, start_state='q0'):
        self.initial_tape = tape
        self.transitions = transitions
        self.head = head_position
        self.state = start_state
        self.running = False
        self.tape = list(tape + '#' * 100)

    def reset(self):
        self.head = 0
        self.state = 'q0'
        self.tape = list(self.initial_tape + '#' * 100)
        self.running = False

    def step(self):
        if self.state == 'HALT':
            return False

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            self.tape[self.head] = new_symbol
            self.state = new_state
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head = max(0, self.head - 1)
            return True
        else:
            self.state = 'HALT'
            return False


class TuringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎛️ Fun Turing Machine Simulator")
        self.machine = None
        self.running_thread = None
        self.auto_run = False
        self.speed = 500
        self.create_widgets()

    def create_widgets(self):
        # Tape Entry
        tk.Label(self.root, text="🧾 Initial Tape:").pack()
        self.tape_entry = tk.Entry(self.root, width=60)
        self.tape_entry.insert(0, "101+011")
        self.tape_entry.pack()

        # Transition Rules
        tk.Label(self.root, text="🔁 Transitions (Format: state symbol -> new_state write_direction L/R):").pack()
        self.transition_text = tk.Text(self.root, height=8, width=70)
        self.transition_text.insert(tk.END, """q0 1 -> q0 1 R
q0 + -> q1 + R
q1 1 -> q1 1 R
q1 # -> HALT # S""")
        self.transition_text.pack()

        # Buttons and Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="▶ Start", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="⏭ Step", command=self.step).pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(control_frame, text="⏸ Pause", command=self.toggle_auto_run, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🔁 Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        # Speed Control
        speed_frame = tk.Frame(self.root)
        speed_frame.pack()
        tk.Label(speed_frame, text="⏱ Animation Speed (ms):").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(500)
        self.speed_scale.pack(side=tk.LEFT)

        # Tape Visual
        self.canvas = tk.Canvas(self.root, width=800, height=100, bg="#f9f9f9")
        self.canvas.pack(pady=10)

        # State Info
        self.state_label = tk.Label(self.root, text="Current State: q0", font=("Arial", 14, "bold"), fg="blue")
        self.state_label.pack()

        # Help
        tk.Label(self.root, text="💡 Example: q0 1 -> q0 1 R means: if in state q0 and reading 1, write 1, move Right, and go to q0").pack()

    def draw_tape(self):
        self.canvas.delete("all")
        if not self.machine:
            return

        start = max(0, self.machine.head - 15)
        end = start + 30
        for i, symbol in enumerate(self.machine.tape[start:end], start=start):
            x0 = (i - start) * 25 + 10
            y0 = 10
            x1 = x0 + 25
            y1 = 60
            fill = "#FFD700" if i == self.machine.head else "white"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=symbol, font=("Consolas", 14, "bold"))

        self.state_label.config(
            text=f"Current State: {self.machine.state}",
            fg="red" if self.machine.state == "HALT" else "green"
        )

    def parse_transitions(self):
        raw = self.transition_text.get("1.0", tk.END).strip().split('\n')
        transitions = {}
        for line in raw:
            if '->' not in line:
                continue
            try:
                left, right = line.split('->')
                state, symbol = left.strip().split()
                new_state, write, move = right.strip().split()
                transitions[(state, symbol)] = (new_state, write, move)
            except:
                messagebox.showerror("Error", f"Invalid transition format: {line}")
                return None
        return transitions

    def start(self):
        transitions = self.parse_transitions()
        if transitions is None:
            return
        tape = self.tape_entry.get()
        self.machine = TuringMachine(tape, transitions)
        self.draw_tape()
        self.auto_run = True
        self.pause_button.config(state=tk.NORMAL)
        self.run_auto()

    def run_auto(self):
        def loop():
            while self.auto_run and self.machine and self.machine.state != "HALT":
                success = self.machine.step()
                self.draw_tape()
                time.sleep(self.speed / 1000)
            self.auto_run = False
        self.running_thread = threading.Thread(target=loop)
        self.running_thread.start()

    def toggle_auto_run(self):
        self.auto_run = not self.auto_run
        if self.auto_run:
            self.pause_button.config(text="⏸ Pause")
            self.run_auto()
        else:
            self.pause_button.config(text="▶ Resume")

    def step(self):
        if self.machine:
            self.machine.step()
            self.draw_tape()

    def reset(self):
        if self.machine:
            self.machine.reset()
            self.draw_tape()
        self.auto_run = False
        self.pause_button.config(text="⏸ Pause", state=tk.DISABLED)

    def update_speed(self, val):
        self.speed = int(val)

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringGUI(root)
    root.mainloop()
