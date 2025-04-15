import tkinter as tk
from tkinter import messagebox

def open_rubiks_gui():
    # Define color palette and mapping
    color_palette = [
        "gray", "green", "red", "blue", "orange", "white", "yellow", "purple", "pink", "cyan", "black"
    ]

    color_ids = {None: 0}
    for idx, color in enumerate(color_palette):
        print(idx, color)
        color_ids[color] = idx

    # Cube face layout
    face_positions = {
        'U': (0, 3),
        'L': (3, 0),
        'F': (3, 3),
        'R': (3, 6),
        'B': (3, 9),
        'D': (6, 3),
    }

    # Storage for the result
    result = {}

    class RubiksCubeGUI:
        def __init__(self, root):
            self.root = root
            self.selected_color = "gray"  # Default color
            self.buttons = {}
            self.grid = {}  # (row, col) -> color string
            self.done_pressed = False

            self.create_palette()
            self.create_cube_grid()

        def create_palette(self):
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text="Color Palette:").pack(side=tk.LEFT)

            for color in color_palette:
                btn = tk.Button(frame, bg=color, width=2, command=lambda c=color: self.set_color(c))
                btn.pack(side=tk.LEFT, padx=2)

        def set_color(self, color):
            self.selected_color = color

        def create_cube_grid(self):
            grid_frame = tk.Frame(self.root)
            grid_frame.pack(pady=10)

            for face, (r_start, c_start) in face_positions.items():
                for i in range(3):
                    for j in range(3):
                        r = r_start + i
                        c = c_start + j
                        btn = tk.Button(grid_frame, width=4, height=2, bg="gray", command=lambda x=r, y=c: self.paint_tile(x, y))
                        btn.grid(row=r, column=c, padx=1, pady=1)
                        self.buttons[(r, c)] = btn
                        self.grid[(r, c)] = "gray"

            # Buttons below the grid
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(pady=5)

            tk.Button(btn_frame, text="Done", command=self.finish).pack(side=tk.LEFT, padx=5)

        def paint_tile(self, r, c):
            if self.selected_color:
                self.buttons[(r, c)].config(bg=self.selected_color)
                self.grid[(r, c)] = self.selected_color

        def show_ids(self):
            ids = {}
            for (r, c), color in self.grid.items():
                ids[(r, c)] = color_ids.get(color, 0)
            msg = "\n".join([f"({r},{c}): ID {id}" for (r, c), id in ids.items()])
            messagebox.showinfo("Sticker IDs", msg)

        def finish(self):
            # Save result and quit
            for (r, c), color in self.grid.items():
                result[(r, c)] = color_ids.get(color, 0)
            self.root.quit()
            self.root.destroy()

    root = tk.Tk()
    root.title("Rubik's Cube Painter")
    app = RubiksCubeGUI(root)
    root.mainloop()
    return result


if __name__ == "__main__":
    result = open_rubiks_gui()
    order = [
        (3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5),
        (3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8),
        (3,9), (3,10), (3,11), (4,9), (4,10), (4,11), (5,9), (5,10), (5,11),
        (3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2),
        (0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5),
        (6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5),
    ]
    print("Copy paste this cubestate into the solver:")
    print(f"np.array([{result[order[0]]}",end="")
    for pos in order[1:]:
        print(f",{result[pos]}",end="")
    print("])")
