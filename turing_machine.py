import tkinter as tk
from tkinter import messagebox
import time
import threading
import math

class TuringMachine:
    def __init__(self, tape, transitions, head_position=0, start_state='q0'):
        self.initial_tape = tape
        self.transitions = transitions
        self.head = head_position
        self.state = start_state
        self.running = False
        self.tape = list(tape + '#' * 100)
        self.step_count = 0

    def reset(self):
        self.head = 0
        self.state = 'q0'
        self.tape = list(self.initial_tape + '#' * 100)
        self.running = False
        self.step_count = 0

    def step(self):
        if self.state == 'HALT':
            return False, "Machine halted."

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            explanation = (
                f"Step {self.step_count + 1}: In state {self.state}, reading '{symbol}' -> "
                f"Write '{new_symbol}', move {direction}, go to {new_state}"
            )
            self.tape[self.head] = new_symbol
            self.state = new_state
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head = max(0, self.head - 1)
            self.step_count += 1
            return True, explanation
        else:
            self.state = 'HALT'
            return False, f"Step {self.step_count}: No transition for ({self.state}, {symbol}). Halting."

class TuringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎛️ Fun Turing Machine Simulator with Graph")
        self.machine = None
        self.running_thread = None
        self.auto_run = False
        self.speed = 500
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        left_frame = tk.Frame(top_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack()

        tk.Label(left_frame, text="🧾 Initial Tape:").pack()
        self.tape_entry = tk.Entry(left_frame, width=40)
        self.tape_entry.insert(0, "101+011")
        self.tape_entry.pack()

        tk.Label(left_frame, text="🔁 Transitions (state symbol -> new_state write dir):").pack()
        self.transition_text = tk.Text(left_frame, height=8, width=50)
        self.transition_text.insert(tk.END, """q0 1 -> q0 1 R
q0 + -> q1 + R
q1 1 -> q1 1 R
q1 # -> HALT # S""")
        self.transition_text.pack()

        control_frame = tk.Frame(left_frame)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="▶ Start", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="⏭ Step", command=self.step).pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(control_frame, text="⏸ Pause", command=self.toggle_auto_run, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🔁 Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        speed_frame = tk.Frame(left_frame)
        speed_frame.pack()
        tk.Label(speed_frame, text="⏱ Speed (ms):").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(500)
        self.speed_scale.pack(side=tk.LEFT)

        tk.Label(left_frame, text="📚 Explanation").pack()
        self.explain_text = tk.Text(left_frame, height=6, width=50, bg="#f0f0ff")
        self.explain_text.pack()

        self.tape_canvas = tk.Canvas(bottom_frame, width=800, height=80, bg="#f9f9f9")
        self.tape_canvas.pack(pady=10)

        self.state_label = tk.Label(bottom_frame, text="State: q0", font=("Arial", 14, "bold"))
        self.state_label.pack()

        tk.Label(right_frame, text="📊 State Graph").pack()
        self.graph_canvas = tk.Canvas(right_frame, width=400, height=300, bg="#ffffff")
        self.graph_canvas.pack()

    def draw_tape(self):
        self.tape_canvas.delete("all")
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
            self.tape_canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            self.tape_canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=symbol, font=("Consolas", 14, "bold"))

        self.state_label.config(
            text=f"State: {self.machine.state}",
            fg="red" if self.machine.state == "HALT" else "green"
        )

    def draw_graph(self):
        self.graph_canvas.delete("all")
        transitions = self.parse_transitions()
        if not transitions:
            return

        states = list(set([s for s, _ in transitions.keys()] + [ns for ns, _, _ in transitions.values()]))
        angle_step = 2 * math.pi / len(states)
        radius = 100
        center_x, center_y = 200, 150
        positions = {}

        for i, state in enumerate(states):
            x = center_x + radius * math.cos(i * angle_step)
            y = center_y + radius * math.sin(i * angle_step)
            positions[state] = (x, y)
            self.graph_canvas.create_oval(x-20, y-20, x+20, y+20, fill="#cce5ff" if state != "HALT" else "#ffcccc")
            self.graph_canvas.create_text(x, y, text=state)

        for (s1, sym), (s2, _, _) in transitions.items():
            x1, y1 = positions[s1]
            x2, y2 = positions[s2]
            self.graph_canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.graph_canvas.create_text(mx, my, text=sym, fill="blue", font=("Arial", 8))

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
        self.draw_graph()
        self.auto_run = True
        self.pause_button.config(state=tk.NORMAL)
        self.run_auto()

    def run_auto(self):
        def loop():
            while self.auto_run and self.machine and self.machine.state != "HALT":
                success, explain = self.machine.step()
                self.draw_tape()
                self.explain_text.insert(tk.END, explain + "\n")
                self.explain_text.see(tk.END)
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
            success, explain = self.machine.step()
            self.draw_tape()
            self.explain_text.insert(tk.END, explain + "\n")
            self.explain_text.see(tk.END)

    def update_speed(self, val):
        self.speed = int(val)

    def reset(self):
        if self.machine:
            self.machine.reset()
            self.draw_tape()
            self.explain_text.delete("1.0", tk.END)
            self.pause_button.config(state=tk.DISABLED, text="⏸ Pause")
            self.auto_run = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringGUI(root)
    root.mainloop()
