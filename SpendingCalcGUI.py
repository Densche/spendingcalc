import tkinter as tk
from tkinter import messagebox
from SpendingCalc import earliest_spend_year, earliest_monthly_spend

def calculate():
    try:
        C = float(entry_C.get())
        r = float(entry_r.get())
        G = float(entry_G.get())
        T = int(entry_T.get())
        withdrawal_type = var.get()

        if withdrawal_type == "lump-sum":
            A = float(entry_A.get())
            x, final_amount = earliest_spend_year(C, r, G, T, A)
            if x is None:
                result.set(f"Not possible to spend {A} and reach the goal.")
            else:
                result.set(f"You can spend {A} in year {x} and still reach {G}. Final: {final_amount:.2f}")
        else:
            M = float(entry_M.get())
            m, final_amount = earliest_monthly_spend(C, r, G, T, M)
            if m is None:
                result.set(f"Not possible to spend {M} monthly and reach the goal.")
            else:
                years = m // 12
                months = m % 12
                result.set(f"Start spending {M} monthly from year {years}, month {months}. Final: {final_amount:.2f}")
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numerical values.")

root = tk.Tk()
root.title("Spending Calculator")

tk.Label(root, text="Initial Capital (C):").grid(row=0, column=0)
entry_C = tk.Entry(root)
entry_C.grid(row=0, column=1)
entry_C.insert(0, "20000")  # Set default value

tk.Label(root, text="Annual Performance (r):").grid(row=1, column=0)
entry_r = tk.Entry(root)
entry_r.grid(row=1, column=1)
entry_r.insert(0, "0.09")  # Set default value

tk.Label(root, text="Target Amount (G):").grid(row=2, column=0)
entry_G = tk.Entry(root)
entry_G.grid(row=2, column=1)
entry_G.insert(0, "200000")  # Set default value

tk.Label(root, text="Total Years (T):").grid(row=3, column=0)
entry_T = tk.Entry(root)
entry_T.grid(row=3, column=1)
entry_T.insert(0, "30")  # Set default value

var = tk.StringVar(value="lump-sum")
tk.Radiobutton(root, text="Lump-Sum Withdrawal", variable=var, value="lump-sum").grid(row=4, column=0)
tk.Radiobutton(root, text="Monthly Withdrawal", variable=var, value="monthly").grid(row=4, column=1)

tk.Label(root, text="Lump-Sum Amount (A):").grid(row=5, column=0)
entry_A = tk.Entry(root)
entry_A.grid(row=5, column=1)
entry_A.insert(0, "1000")  # Set default value

tk.Label(root, text="Monthly Withdrawal (M):").grid(row=6, column=0)
entry_M = tk.Entry(root)
entry_M.grid(row=6, column=1)
entry_M.insert(0, "200")  # Set default value

btn_calculate = tk.Button(root, text="Calculate", command=calculate)
btn_calculate.grid(row=7, column=0, columnspan=2)

result = tk.StringVar()
result_label = tk.Label(root, textvariable=result, fg="blue")
result_label.grid(row=8, column=0, columnspan=2)

root.mainloop()
