import tkinter as tk

BG = "#0d1526"
HEADER = "#0f2436"
PANEL = "#111727"
EDITOR_BG = "#0f2030"
TERMINAL_BG = "#0b1a29"
CARD = "#18253a"
AQUA = "#23e4d8"
WHITE = "#e6eef8"
SUBTLE = "#2a3a4a"

DOT_RED = "#e25757"
DOT_YELLOW = "#5dd06a"
DOT_GREEN = "#63e0c6"

WIDTH = 1366
HEIGHT = 768


def rounded_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y1+r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class GoSimulatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Go Simulator")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.build_gui()

   
    def build_gui(self):

        header_h = 70
        header_frame = tk.Frame(self.root, bg=HEADER, height=header_h)
        header_frame.pack(fill="x", side="top")

        left_container = tk.Frame(header_frame, bg=HEADER)
        left_container.place(x=20, y=10, height=header_h-20)

        icon_label = tk.Label(left_container, text=">_", fg=AQUA, bg=HEADER,
                              font=("Consolas", 18, "bold"))
        icon_label.pack(side="left", padx=(6, 8))

        title_go = tk.Label(left_container, text="Go ", fg=WHITE, bg=HEADER,
                            font=("Segoe UI", 14, "bold"))
        title_go.pack(side="left")

        title_sim = tk.Label(left_container, text="Simulator", fg=AQUA, bg=HEADER,
                             font=("Segoe UI", 14, "bold"))
        title_sim.pack(side="left")

        run_w = 110
        run_h = 42
        run_x = WIDTH - run_w - 30
        run_y = 14

        run_can = tk.Canvas(header_frame, width=run_w, height=run_h,
                            bg=HEADER, highlightthickness=0)
        run_can.place(x=run_x, y=run_y)

        rounded_rect(run_can, 0, 0, run_w, run_h, r=8, fill=AQUA, outline=AQUA)
        run_can.create_text(run_w/2 + 6, run_h/2, text="▶ Run",
                            font=("Segoe UI", 11, "bold"),
                            fill="#073b4c")

        run_can.bind("<Button-1>", self._run_clicked)

        sep = tk.Frame(self.root, bg=SUBTLE, height=2)
        sep.pack(fill="x", side="top")

        main_pad_x = 30
        editor_h = 430
        editor_w = WIDTH - 2*main_pad_x

        main_container = tk.Frame(self.root, bg=BG)
        main_container.pack(fill="both", expand=False,
                            padx=main_pad_x, pady=(18, 10))

        editor_canvas = tk.Canvas(main_container, width=editor_w,
                                  height=editor_h, bg=BG,
                                  highlightthickness=0)
        editor_canvas.pack()

        rounded_rect(editor_canvas, 0, 0, editor_w, editor_h,
                     r=12, fill=PANEL, outline=SUBTLE)

        pad = 18
        rounded_rect(editor_canvas, pad, pad+12,
                     editor_w-pad, editor_h-pad,
                     r=10, fill=EDITOR_BG, outline="")

        tab_h = 36
        tab_w = 240
        tab_x = pad + 8
        tab_y = pad + 6

        editor_canvas.create_rectangle(tab_x, tab_y,
                                       tab_x + tab_w, tab_y + tab_h,
                                       fill=CARD, outline="")

        dot_r = 6
        dot_midy = tab_y + tab_h/2

        editor_canvas.create_oval(tab_x + 10 - dot_r, dot_midy - dot_r,
                                  tab_x + 10 + dot_r, dot_midy + dot_r,
                                  fill=DOT_RED, outline="")
        editor_canvas.create_oval(tab_x + 30 - dot_r, dot_midy - dot_r,
                                  tab_x + 30 + dot_r, dot_midy + dot_r,
                                  fill=DOT_YELLOW, outline="")
        editor_canvas.create_oval(tab_x + 50 - dot_r, dot_midy - dot_r,
                                  tab_x + 50 + dot_r, dot_midy + dot_r,
                                  fill=DOT_GREEN, outline="")

        editor_canvas.create_text(tab_x + 110, tab_midy := (tab_y + tab_h/2),
                                  text="main.go", anchor="w",
                                  fill="#8fa4bf", font=("Segoe UI", 10))

        editor_x = pad + 12
        editor_y = pad + tab_h + 20
        editor_width = editor_w - 2*(pad+12)
        editor_height = editor_h - (tab_h + pad + 34)

        editor_frame = tk.Frame(editor_canvas, bg=EDITOR_BG)
        editor_canvas.create_window(editor_x, editor_y, anchor="nw",
                                    window=editor_frame,
                                    width=editor_width,
                                    height=editor_height)

        self.editor_text = tk.Text(editor_frame,
                                   bg=EDITOR_BG, fg=WHITE,
                                   insertbackground=WHITE,
                                   font=("Consolas", 13),
                                   bd=0, padx=14, pady=12,
                                   wrap="none",
                                   highlightthickness=0)
        self.editor_text.pack(fill="both", expand=True)

        self.editor_text.insert("1.0", """package main
import "fmt"

func main(){
    fmt.Println("Hola Mundo!")
}
""")

        term_h = 170
        term_canvas = tk.Canvas(main_container, width=editor_w,
                                height=term_h, bg=BG,
                                highlightthickness=0)
        term_canvas.pack(pady=(20, 0))

        rounded_rect(term_canvas, 0, 0, editor_w, term_h,
                     r=12, fill=PANEL, outline=SUBTLE)

        tpad = 10
        term_canvas.create_rectangle(tpad, tpad,
                                     editor_w - tpad, tpad + 36,
                                     fill=CARD, outline="")

        term_canvas.create_text(tpad + 18, tpad + 18, text=">_",
                                fill=AQUA, font=("Consolas", 11, "bold"),
                                anchor="w")
        term_canvas.create_text(tpad + 48, tpad + 18, text="Terminal",
                                fill=WHITE, font=("Segoe UI", 10),
                                anchor="w")

        term_text_x = tpad
        term_text_y = tpad + 44
        term_text_w = editor_w - 2*tpad
        term_text_h = term_h - (tpad + 54)

        terminal_frame = tk.Frame(term_canvas, bg=TERMINAL_BG)
        term_canvas.create_window(term_text_x, term_text_y, anchor="nw",
                                  window=terminal_frame,
                                  width=term_text_w,
                                  height=term_text_h)

        self.terminal_text = tk.Text(
            terminal_frame,
            bg=TERMINAL_BG,
            fg="#95f5d6",
            insertbackground=WHITE,
            font=("Consolas", 11),
            bd=0, padx=12, pady=12,
            wrap="word",
            state="disabled",
            highlightthickness=0
        )
        self.terminal_text.pack(fill="both", expand=True)

    
    def _run_clicked(self, event=None):
        self.terminal_text.config(state="normal")
        self.terminal_text.delete("1.0", "end")
        self.terminal_text.insert("end", "$ go run main.go\n\nEjecutando código...\n\n")
        content = self.editor_text.get("1.0", "end")
        self.terminal_text.insert("end", content)
        self.terminal_text.config(state="disabled")

    def write_terminal(self, msg: str):
        self.terminal_text.config(state="normal")
        self.terminal_text.insert("end", msg + "\n")
        self.terminal_text.see("end")
        self.terminal_text.config(state="disabled")

    def get_code(self):
        return self.editor_text.get("1.0", "end").strip()
