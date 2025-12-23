import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

times = []
kwh_values = []

#visuals
BG_COLOR = "#b6e3b6"   # soft green
FONT_MAIN = ("Georgia", 11)
FONT_TITLE = ("Georgia", 14, "bold")

#load csv
def load_file():
    global times, kwh_values
    times = []
    kwh_values = []

    file_path = filedialog.askopenfilename(
        title="Select Energy Usage CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            if "time" not in reader.fieldnames or "kwh" not in reader.fieldnames:
                messagebox.showerror(
                    "Error",
                    "CSV must contain 'time' and 'kwh' columns."
                )
                return

            for row in reader:
                times.append(row["time"])
                kwh_values.append(float(row["kwh"]))

        status_label.config(text="File loaded successfully.")
        analyze_data()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")

#energy data
def analyze_data():
    if not kwh_values:
        return

    total_energy = sum(kwh_values)
    average_usage = total_energy / len(kwh_values)

    peak_kwh = max(kwh_values)
    peak_index = kwh_values.index(peak_kwh)
    peak_time = times[peak_index]

    threshold = 1.5 * average_usage

    total_label.config(text=f"Total Energy: {total_energy:.2f} kWh")
    avg_label.config(text=f"Average Usage: {average_usage:.2f} kWh")
    peak_label.config(text=f"Peak Usage: {peak_kwh:.2f} kWh at {peak_time}")

    high_usage_box.delete("1.0", tk.END)
    found = False

    for i in range(len(kwh_values)):
        if kwh_values[i] > threshold:
            high_usage_box.insert(
                tk.END,
                f"{times[i]} → {kwh_values[i]} kWh\n"
            )
            found = True

    if not found:
        high_usage_box.insert(tk.END, "No unusually high usage detected.")

#plot
def show_plot():
    if not kwh_values:
        messagebox.showerror("Error", "No data loaded.")
        return

    plt.plot(times, kwh_values)
    plt.xlabel("Time")
    plt.ylabel("Energy Usage (kWh)")
    plt.title("Hourly Energy Consumption")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#GUI
root = tk.Tk()
root.title("Energy Usage Analyzer")
root.geometry("600x520")
root.configure(bg=BG_COLOR)

#title
title_label = tk.Label(
    root,
    text="Energy Usage Analyzer",
    font=FONT_TITLE,
    bg=BG_COLOR
)
title_label.pack(pady=10)

#buttons
load_button = tk.Button(
    root,
    text="Select Energy CSV File",
    font=FONT_MAIN,
    command=load_file
)
load_button.pack(pady=5)

plot_button = tk.Button(
    root,
    text="Show Energy Plot",
    font=FONT_MAIN,
    command=show_plot
)
plot_button.pack(pady=5)

#summary labels
total_label = tk.Label(root, text="Total Energy: --", font=FONT_MAIN, bg=BG_COLOR)
total_label.pack()

avg_label = tk.Label(root, text="Average Usage: --", font=FONT_MAIN, bg=BG_COLOR)
avg_label.pack()

peak_label = tk.Label(root, text="Peak Usage: --", font=FONT_MAIN, bg=BG_COLOR)
peak_label.pack()

#high usage section
high_label = tk.Label(
    root,
    text="High Usage Periods (Potential Inefficiencies):",
    font=FONT_MAIN,
    bg=BG_COLOR
)
high_label.pack(pady=10)

high_usage_box = tk.Text(
    root,
    height=8,
    width=60,
    font=FONT_MAIN
)
high_usage_box.pack()

status_label = tk.Label(
    root,
    text="No file loaded.",
    font=FONT_MAIN,
    bg=BG_COLOR,
    fg="darkgreen"
)
status_label.pack(pady=10)

root.mainloop()
