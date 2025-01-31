import tkinter as tk
from tkinter import messagebox
from SpendingCalc import earliest_spend_year, earliest_monthly_spend

# ---- 1) ADD MATPLOTLIB IMPORTS
import matplotlib
matplotlib.use("TkAgg")  # Use the TkAgg backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def calculate():
    try:
        # === Read user inputs ===
        C = float(entry_C.get())
        r_percent = float(entry_r.get())       # e.g. 9 for 9%
        G = float(entry_G.get())
        T = int(entry_T.get())
        withdrawal_type = var.get()

        # Convert percentage to decimal for intermediate calculations
        r = r_percent / 100.0

        # === Compute "No Spending" baseline ===
        capital_no_spend = compute_no_spend_trajectory(C, r, T, withdrawal_type)

        # === Depending on the chosen withdrawal type, compute earliest spending info ===
        if withdrawal_type == "lump-sum":
            A = float(entry_A.get())  # Lump-sum withdrawal
            x, final_amount = earliest_spend_year(C, r_percent, G, T, A)

            if x is None:
                # Not possible
                result.set(
                    f"\nIt's not possible to spend {A} and still reach the goal.\n\n"
                    f"Without spending, you'd have {capital_no_spend[-1]:.2f} by year {T}.\n"
                )
                plot_graph([], [], list(range(T+1)), capital_no_spend, withdrawal_type)
            else:
                # Possible
                result.set(
                    f"\n✅ Possible!\n\n"
                    f"💰 You can spend {A} at year {x} (or later) and still reach {G} by year {T}.\n"
                    f"📊 Final amount: {final_amount:.2f}\n"
                    f"📈 Without spending, you'd have {capital_no_spend[-1]:.2f}.\n"
                )
                # === Compute the capital path for the "with spending" scenario ===
                capital_with_spend = compute_lumpsum_trajectory(C, r, T, A, x)
                # === Plot both lines ===
                plot_graph(list(range(T+1)), capital_with_spend,
                           list(range(T+1)), capital_no_spend,
                           withdrawal_type)

        else:
            # Monthly scenario
            M = float(entry_M.get())
            m, final_amount = earliest_monthly_spend(C, r_percent, G, T, M)

            if m is None:
                result.set(
                    f"\nIt's not possible to spend {M} monthly and still reach the goal.\n\n"
                    f"Without spending, you'd have {capital_no_spend[-1]:.2f} by year {T}.\n"
                )
                plot_graph([], [], list(range(T+1)), capital_no_spend, withdrawal_type)
            else:
                years = m // 12
                months = m % 12
                result.set(
                    f"\n✅ Possible!\n\n"
                    f"📅 You can start spending {M} monthly from year {years}, month {months}.\n"
                    f"📊 Final amount: {final_amount:.2f}\n"
                    f"📈 Without spending, you'd have {capital_no_spend[-1]:.2f}.\n"
                )
                # === Compute the monthly capital path for the "with spending" scenario ===
                capital_with_spend_monthly = compute_monthly_trajectory(C, r, T, M, m)
                # === Plot both lines (month by month) ===
                plot_graph(list(range(T*12 + 1)), capital_with_spend_monthly,
                           list(range(T*12 + 1)), compute_no_spend_trajectory(C, r, T, "monthly"),
                           withdrawal_type)

    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numerical values.")


# ------------------------------------------------------------------
# HELPER: Compute the capital trajectory with NO spending
#   - For "lump-sum", we do a year-by-year path
#   - For "monthly", we do a month-by-month path
# ------------------------------------------------------------------
def compute_no_spend_trajectory(C, r, T, withdrawal_type):
    """
    Returns a list of capital values over time WITHOUT any spending,
    either year-by-year or month-by-month depending on 'withdrawal_type'.
    """
    if withdrawal_type == "lump-sum":
        # Yearly
        trajectory = []
        capital = C
        for year in range(T+1):
            if year == 0:
                trajectory.append(capital)
            else:
                capital = capital * (1 + r)
                trajectory.append(capital)
        return trajectory

    else:  # "monthly"
        # Month-by-month
        monthly_r = (1 + r) ** (1/12) - 1
        total_months = T * 12
        trajectory = []
        capital = C
        for month in range(total_months + 1):
            if month == 0:
                trajectory.append(capital)
            else:
                capital = capital * (1 + monthly_r)
                trajectory.append(capital)
        return trajectory


# ------------------------------------------------------------------
# HELPER: Compute the capital trajectory for LUMP-SUM scenario
# ------------------------------------------------------------------
def compute_lumpsum_trajectory(C, r, T, A, spend_year):
    """
    Returns a list of capital values (year-by-year) when you
    spend 'A' in 'spend_year'.
    """
    trajectory = []
    capital = C
    for year in range(T+1):
        if year == 0:
            trajectory.append(capital)
        else:
            # Growth first
            capital = capital * (1 + r)
            # If we hit the spend_year, subtract A once
            if year == spend_year:
                capital -= A
            trajectory.append(capital)
    return trajectory


# ------------------------------------------------------------------
# HELPER: Compute the capital trajectory for MONTHLY scenario
# ------------------------------------------------------------------
def compute_monthly_trajectory(C, r, T, M, start_month):
    """
    Returns a list of capital values (month-by-month) when you
    start spending 'M' every month from 'start_month' onward.
    """
    monthly_r = (1 + r) ** (1/12) - 1
    total_months = T * 12

    trajectory = []
    capital = C
    for month in range(total_months + 1):
        # Record capital at the *start* of the month
        trajectory.append(capital)

        if month < total_months:  # If we haven't reached the last point
            # Only subtract M if we're >= start_month
            if month >= start_month:
                capital -= M
                if capital < 0:
                    # If it ever goes negative, break or keep it negative
                    # but let's just keep it for completeness
                    # so we can see it dipping below zero in the plot
                    pass
            capital = capital * (1 + monthly_r)

    return trajectory


# ------------------------------------------------------------------
# MATPLOTLIB PLOTTING
# ------------------------------------------------------------------
def plot_graph(x_spend, y_spend, x_no_spend, y_no_spend, withdrawal_type):
    """
    Plot two lines on the embedded matplotlib chart:
     - "With spending" (x_spend vs y_spend)
     - "No spending"   (x_no_spend vs y_no_spend)
    """
    # Clear the previous figure
    ax.clear()

    if len(x_spend) > 0:
        ax.plot(x_spend, y_spend, label="With Spending", color="red")
    ax.plot(x_no_spend, y_no_spend, label="No Spending", color="green")

    ax.set_xlabel("Time" + (" (Months)" if withdrawal_type=="monthly" else " (Years)"))
    ax.set_ylabel("Capital")
    ax.set_title("Capital Development Over Time")
    ax.legend()

    # Refresh the canvas
    canvas.draw()


# ========================
#     TKINTER UI SETUP
# ========================

root = tk.Tk()
root.title("Spending Calculator")
root.geometry("1400x700")
root.configure(bg="#e6f4ea")

main_frame = tk.Frame(root, bg="#d4edda", padx=20, pady=20, relief="ridge", bd=2)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

def create_label(text, row, column):
    label = tk.Label(main_frame, text=text, bg="#d4edda", fg="#2a5934",
                     font=("Segoe UI", 13, "bold"))
    label.grid(row=row, column=column, padx=10, pady=8, sticky="w")

def create_entry(default, row, column):
    entry = tk.Entry(main_frame, font=("Segoe UI", 13), bd=0, relief="solid",
                     highlightthickness=1, highlightbackground="#4caf50",
                     highlightcolor="#4caf50", justify="center")
    entry.grid(row=row, column=column, padx=10, pady=8, ipadx=8, ipady=5)
    entry.insert(0, default)
    return entry

# --- Left side input fields ---
create_label("Initial Capital (C):", 0, 0)
entry_C = create_entry("20000", 0, 1)

create_label("Annual Performance (r) [%]:", 1, 0)
entry_r = create_entry("9", 1, 1)

create_label("Target Amount (G):", 2, 0)
entry_G = create_entry("200000", 2, 1)

create_label("Total Years (T):", 3, 0)
entry_T = create_entry("30", 3, 1)

var = tk.StringVar(value="lump-sum")
radio_frame = tk.Frame(main_frame, bg="#d4edda")
radio_frame.grid(row=4, column=0, columnspan=2, pady=8)

tk.Radiobutton(radio_frame, text="Lump-Sum Withdrawal", variable=var,
               value="lump-sum", bg="#d4edda", fg="#2a5934",
               font=("Segoe UI", 12)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Monthly Withdrawal", variable=var,
               value="monthly", bg="#d4edda", fg="#2a5934",
               font=("Segoe UI", 12)).pack(side="left", padx=10)

create_label("Lump-Sum Amount (A):", 5, 0)
entry_A = create_entry("1000", 5, 1)

create_label("Monthly Withdrawal (M):", 6, 0)
entry_M = create_entry("200", 6, 1)

def on_hover(event):
    event.widget.config(bg="#388e3c")

def on_leave(event):
    event.widget.config(bg="#4caf50")

btn_calculate = tk.Button(main_frame, text="Calculate", command=calculate,
                          bg="#4caf50", fg="white", font=("Segoe UI", 13, "bold"),
                          padx=12, pady=6, bd=0, relief="flat")
btn_calculate.grid(row=7, column=0, columnspan=2, pady=12)

btn_calculate.bind("<Enter>", on_hover)
btn_calculate.bind("<Leave>", on_leave)

result = tk.StringVar()
result_label = tk.Label(main_frame, textvariable=result, fg="#2a5934",
                        bg="#d4edda", font=("Segoe UI", 13, "bold"),
                        justify="left", wraplength=500, anchor="w")
result_label.grid(row=8, column=0, columnspan=2, pady=12, padx=10, sticky="w")

# --- Right side chart frame ---
chart_frame = tk.Frame(main_frame, bg="#d4edda")
chart_frame.grid(row=0, column=2, rowspan=9, padx=20, pady=20, sticky="n")

# Create a matplotlib figure & embed in Tkinter
fig = plt.Figure(figsize=(6, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack()

root.mainloop()
