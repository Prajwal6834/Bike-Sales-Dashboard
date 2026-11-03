
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load dataset
df = pd.read_csv('bike_sales_india.csv')

all_cols = df.columns.tolist()
num_cols = df.select_dtypes(include='number').columns.tolist()

# Main window
root = tk.Tk()
root.title("Bike Sales Dashboard")
root.geometry("1100x650")

# Left panel
panel = tk.Frame(root, bg="#263238", padx=15, pady=20)
panel.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(panel, text="BIKE SALES",
         font=("Arial", 18, "bold"),
         bg="#263238", fg="white").pack(pady=20)

# X dropdown
tk.Label(panel, text="X Axis", bg="#263238",
         fg="white").pack(anchor="w")

x_cb = ttk.Combobox(panel, values=all_cols,
                    state="readonly", width=22)
x_cb.set(all_cols[0])
x_cb.pack(pady=10)

# Y dropdown
tk.Label(panel, text="Y Axis", bg="#263238",
         fg="white").pack(anchor="w")

y_cb = ttk.Combobox(panel, values=num_cols,
                    state="readonly", width=22)
y_cb.set(num_cols[0])
y_cb.pack(pady=10)

# Matplotlib graph
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

current_graph = "Line"

# Graph function
def show_graph(graph=None):
    global current_graph

    if graph:
        current_graph = graph

    x = x_cb.get()
    y = y_cb.get()

    ax.clear()

    if current_graph == "Line":
        data = df.groupby(x)[y].mean()
        ax.plot(data.index.astype(str), data.values, marker='o')

    elif current_graph == "Bar":
        data = df.groupby(x)[y].mean()
        ax.bar(data.index.astype(str), data.values, color='blue')

    elif current_graph == "Histogram":
        ax.hist(df[y].dropna(), bins=15,
                color='orange', edgecolor='black')

    elif current_graph == "Scatter":
        data = df[[x, y]].dropna()
        x_data = data[x]

        if not pd.api.types.is_numeric_dtype(x_data):
            x_data = pd.factorize(x_data)[0]

        ax.scatter(x_data, data[y], color='purple')

    ax.set_title(current_graph + " Graph")
    ax.set_xlabel(x if current_graph != "Histogram" else y)
    ax.set_ylabel("Frequency" if current_graph == "Histogram" else y)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    canvas.draw_idle()

# Graph buttons
buttons = [
    ("Line Graph", "Line", "#4CAF50"),
    ("Bar Graph", "Bar", "#2196F3"),
    ("Histogram", "Histogram", "#FF9800"),
    ("Scatter Graph", "Scatter", "#9C27B0")
]

for label, graph, color in buttons:
    tk.Button(
        panel, text=label, bg=color, fg="white",
        font=("Arial", 10, "bold"), width=20,
        pady=8, command=lambda g=graph: show_graph(g)
    ).pack(pady=8)

# Dropdown updates
x_cb.bind("<<ComboboxSelected>>",
          lambda event: show_graph())

y_cb.bind("<<ComboboxSelected>>",
          lambda event: show_graph())

# Initial graph
show_graph()

root.mainloop()
