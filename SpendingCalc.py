import math

def earliest_spend_year(C, r, G, T, A):
    """
    Determines the earliest integer year x (0 <= x <= T) at which you can afford
    to spend amount A in a single lump sum and still end up with >= G at year T.
    Uses a straightforward simulation loop for correctness.

    Parameters
    ----------
    C : float
        Initial capital.
    r : float
        Annual performance (e.g., 0.07 for 7%).
    G : float
        Target amount after T years.
    T : int
        Total number of years.
    A : float
        Lump-sum amount to withdraw once.

    Returns
    -------
    (x, final_amount) : (int or None, float)
        x is the earliest year you can withdraw A and still end up with >= G.
        If it's impossible, returns (None, capital_without_spending).
    """
    # Calculate the capital if you never spend
    final_without_spending = C * (1 + r) ** T

    # If you can't even reach G without spending, no solution
    if final_without_spending < G:
        return None, final_without_spending

    # Try each integer year x from 0 to T
    for x in range(T + 1):
        # Grow capital for x years
        capital_after_x_years = C * (1 + r) ** x
        # Withdraw lump sum A
        capital_after_spending = capital_after_x_years - A
        # If negative, skip (though in principle you could check if it recovers, but let's keep it consistent)
        # Grow for remaining (T - x) years
        final_amount = capital_after_spending * (1 + r) ** (T - x)

        # Check if final is >= G
        if final_amount >= G:
            return x, final_amount

    # If no x works, return None
    return None, final_without_spending

def earliest_monthly_spend(C, r, G, T, M):
    """
    Determines the earliest month m (0 <= m <= 12*T) at which you can start
    withdrawing M every month and still end up with >= G at year T.
    Uses a straightforward month-by-month simulation for correctness.

    Parameters
    ----------
    C : float
        Initial capital.
    r : float
        Annual performance (e.g., 0.07 for 7%).
    G : float
        Target amount after T years.
    T : int
        Total number of years.
    M : float
        Monthly withdrawal amount.

    Returns
    -------
    (m, final_amount) : (int or None, float)
        m is the earliest month you can start withdrawing M and still end up with >= G.
        If it's impossible, returns (None, capital_without_spending).
    """
    monthly_rate = (1 + r) ** (1/12) - 1
    total_months = T * 12

    # Capital if you never spend
    final_without_spending = C * (1 + r) ** T
    if final_without_spending < G:
        return None, final_without_spending

    # For each possible start month m
    for m in range(total_months + 1):
        capital = C

        # 1) Grow capital for m months with no withdrawals
        for _ in range(m):
            capital *= (1 + monthly_rate)

        # 2) Now withdraw M for each of the remaining months
        remaining = total_months - m
        for _ in range(remaining):
            # Withdraw at start of month
            capital -= M
            if capital < 0:
                # No point going further; can't recover from negative if M keeps being withdrawn
                break
            capital *= (1 + monthly_rate)

        # Check if final capital after T years is >= G
        if capital >= G:
            return m, capital

    # If none of the months work, return None
    return None, final_without_spending

# --------------------------------------------------------------------
# Example usage:
if __name__ == "__main__":
    # Example input
    C_input = 10000            # Starting capital 
    r_input = 0.30           # Annual performance  
    G_input = 2000000            # Target capital
    T_input = 20             # Time horizon in years
    A_input = 3000            # Lump-sum withdrawal
    M_input = 500             # Monthly withdrawal

    # Choose withdrawal type: "lump-sum" or "monthly"
    withdrawal_type = "lump-sum"  # or "monthly"

    # Also compute final_without_spending for display
    final_without_spending = C_input * ((1 + r_input) ** T_input)

    if withdrawal_type == "lump-sum":
        x, final_amount = earliest_spend_year(C_input, r_input, G_input, T_input, A_input)
        if x is None:
            print("It's not possible to spend that lump sum and still reach the goal.")
            print(f"Without spending, you'd have {final_without_spending:.2f} by year {T_input}.")
        else:
            print("Possible!")
            print(f"You can spend {A_input} at year {x} (or later) and still reach {G_input} by year {T_input}.")
            print(f"You will reach {final_amount:.2f} by year {T_input}.")
            print(f"If you wouldn't have spent it, you would have {final_without_spending:.2f}.")

    elif withdrawal_type == "monthly":
        m, final_amount = earliest_monthly_spend(C_input, r_input, G_input, T_input, M_input)
        if m is None:
            print("It's not possible to spend that amount monthly and still reach the goal.")
            print(f"Without spending, you'd have {final_without_spending:.2f} by year {T_input}.")
        else:
            years = m // 12
            months = m % 12
            print("Possible!")
            print(f"You can start spending {M_input} monthly from year {years}, month {months},")
            print(f"and still reach {G_input} by year {T_input}.")
            print(f"You will reach {final_amount:.2f} by year {T_input}.")
            print(f"If you wouldn't have spent it, you would have {final_without_spending:.2f}.")
