import tkinter as tk
from tkinter import messagebox
from SpendingCalc import earliest_spend_year, earliest_monthly_spend

def calculate():
    try:
        C = float(entry_C.get())
        r = float(entry_r.get()) / 100  # Convert percentage input to decimal
        G = float(entry_G.get())
        T = int(entry_T.get())
        withdrawal_type = var.get()

        if withdrawal_type == "lump-sum":
            A = float(entry_A.get())
            x, final_amount = earliest_spend_year(C, r * 100, G, T, A)
            if x is None:
                result.set(f"\nIt's not possible to spend {A} and still reach the goal.\n\nWithout spending, you'd have {C * (1 + r) ** T:.2f} by year {T}.\n")
            else:
                result.set(f"\n✅ Possible!\n\n💰 You can spend {A} at year {x} (or later) and still reach {G} by year {T}.\n📊 Final amount: {final_amount:.2f}\n📈 Without spending, you would have {C * (1 + r) ** T:.2f}.\n")
        else:
            M = float(entry_M.get())
            m, final_amount = earliest_monthly_spend(C, r * 100, G, T, M)
            if m is None:
                result.set(f"\nIt's not possible to spend {M} monthly and still reach the goal.\n\nWithout spending, you'd have {C * (1 + r) ** T:.2f} by year {T}.\n")
            else:
                years = m // 12
                months = m % 12
                result.set(f"\n✅ Possible!\n\n📅 You can start spending {M} monthly from year {years}, month {months}.\n📊 Final amount: {final_amount:.2f}\n📈 Without spending, you would have {C * (1 + r) ** T:.2f}.\n")
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numerical values.")

root = tk.Tk()
root.title("Spending Calculator")
root.geometry("1400x700")
root.configure(bg="#e6f4ea")

main_frame = tk.Frame(root, bg="#d4edda", padx=20, pady=20, relief="ridge", bd=2)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

def create_label(text, row, column):
    label = tk.Label(main_frame, text=text, bg="#d4edda", fg="#2a5934", font=("Segoe UI", 13, "bold"))
    label.grid(row=row, column=column, padx=10, pady=8, sticky="w")

def create_entry(default, row, column):
    entry = tk.Entry(main_frame, font=("Segoe UI", 13), bd=0, relief="solid", highlightthickness=1, highlightbackground="#4caf50", highlightcolor="#4caf50", justify="center")
    entry.grid(row=row, column=column, padx=10, pady=8, ipadx=8, ipady=5)
    entry.insert(0, default)
    return entry

create_label("Initial Capital (C):", 0, 0)
entry_C = create_entry("20000", 0, 1)

create_label("Annual Performance (r) [%]:", 1, 0)
entry_r = create_entry("9", 1, 1)  # Changed from "0.09" to "9" (percentage)

create_label("Target Amount (G):", 2, 0)
entry_G = create_entry("200000", 2, 1)

create_label("Total Years (T):", 3, 0)
entry_T = create_entry("30", 3, 1)

var = tk.StringVar(value="lump-sum")
radio_frame = tk.Frame(main_frame, bg="#d4edda")
radio_frame.grid(row=4, column=0, columnspan=2, pady=8)

tk.Radiobutton(radio_frame, text="Lump-Sum Withdrawal", variable=var, value="lump-sum", bg="#d4edda", fg="#2a5934", font=("Segoe UI", 12)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Monthly Withdrawal", variable=var, value="monthly", bg="#d4edda", fg="#2a5934", font=("Segoe UI", 12)).pack(side="left", padx=10)

create_label("Lump-Sum Amount (A):", 5, 0)
entry_A = create_entry("1000", 5, 1)

create_label("Monthly Withdrawal (M):", 6, 0)
entry_M = create_entry("200", 6, 1)

def on_hover(event):
    event.widget.config(bg="#388e3c")

def on_leave(event):
    event.widget.config(bg="#4caf50")


btn_calculate = tk.Button(main_frame, text="Calculate", command=calculate, bg="#4caf50", fg="white", font=("Segoe UI", 13, "bold"), padx=12, pady=6, bd=0, relief="flat")
btn_calculate.grid(row=7, column=0, columnspan=2, pady=12)

btn_calculate.bind("<Enter>", on_hover)
btn_calculate.bind("<Leave>", on_leave)

result = tk.StringVar()
result_label = tk.Label(main_frame, textvariable=result, fg="#2a5934", bg="#d4edda", font=("Segoe UI", 13, "bold"), justify="left", wraplength=500, anchor="w")
result_label.grid(row=8, column=0, columnspan=2, pady=12, padx=10, sticky="w")

root.mainloop()
