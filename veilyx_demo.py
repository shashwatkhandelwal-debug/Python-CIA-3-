import math
import os
import json
from datetime import datetime

GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
MAGENTA = "\033[95m"
RESET   = "\033[0m"

DATA_FILE = "investments.json"

# ══════════════════════════════════════════════
#  FILE HANDLING
# ══════════════════════════════════════════════

def load_investments():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"username": "Investor", "saved_plans": []}

def save_investments(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ══════════════════════════════════════════════
#  DISPLAY HELPERS
# ══════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=60):
    print(f"{DIM}{char * width}{RESET}")

def header(title):
    width = 60
    print(f"\n{CYAN}{BOLD}{'═' * width}{RESET}")
    pad = (width - len(title)) // 2
    print(f"{CYAN}{BOLD}{' ' * pad}{title}{RESET}")
    print(f"{CYAN}{'═' * width}{RESET}\n")

# ══════════════════════════════════════════════
#  CORE FORMULA FUNCTIONS
# ══════════════════════════════════════════════

def compound_interest(principal, rate, n, t):
    """
    Formula: A = P * (1 + r/n)^(n*t)
    P = principal, r = annual rate (decimal),
    n = compounding frequency, t = time in years
    """
    amount   = principal * math.pow((1 + rate / n), n * t)
    interest = amount - principal
    return round(amount, 2), round(interest, 2)

def compound_with_monthly_sip(principal, monthly_sip, rate, n, t):
    """
    Combines lump sum + monthly deposit
    SIP Future Value = SIP * [((1 + r/n)^(n*t) - 1) / (r/n)]
    """
    lump_amount  = principal * math.pow((1 + rate / n), n * t)
    r_per_period = rate / 12
    periods      = int(t * 12)
    if r_per_period > 0:
        sip_amount = monthly_sip * ((math.pow(1 + r_per_period, periods) - 1) / r_per_period) * (1 + r_per_period)
    else:
        sip_amount = monthly_sip * periods
    total          = lump_amount + sip_amount
    total_invested = principal + (monthly_sip * periods)
    interest       = total - total_invested
    return round(total, 2), round(interest, 2), round(total_invested, 2)

def yearly_breakdown(principal, rate, n, t):
    """Return a list of (year, amount, interest_earned) for each year."""
    breakdown = []
    for year in range(1, int(t) + 1):
        amount, interest = compound_interest(principal, rate, n, year)
        breakdown.append({"year": year, "amount": amount, "interest": interest})
    return breakdown

# ══════════════════════════════════════════════
#  ASCII BAR CHART
# ══════════════════════════════════════════════

def bar_chart(breakdown, principal):
    """Year-by-year chart showing amount, yearly interest and monthly interest."""
    max_amount = breakdown[-1]["amount"]
    max_bar    = 25

    print(f"\n  {BOLD}Year-by-Year Growth Chart{RESET}\n")
    print(f"  {'YEAR':<6} {'AMOUNT':>14}  {'INT/YEAR':>11}  {'INT/MONTH':>11}  GROWTH BAR")
    divider()

    for entry in breakdown:
        year             = entry["year"]
        amount           = entry["amount"]
        interest_yearly  = entry["interest"]
        interest_monthly = round(interest_yearly / 12, 2)

        pct     = amount / max_amount
        bar_len = int(pct * max_bar)

        if pct < 0.4:
            color = YELLOW
        elif pct < 0.75:
            color = CYAN
        else:
            color = GREEN

        bar = "█" * bar_len + f"{DIM}░{RESET}" * (max_bar - bar_len)

        print(f"  Yr {year:<3} {BOLD}₹{amount:>12,.0f}{RESET}  "
              f"{CYAN}₹{interest_yearly:>9,.2f}{RESET}  "
              f"{MAGENTA}₹{interest_monthly:>9,.2f}{RESET}  "
              f"{color}{bar}{RESET}")

# ══════════════════════════════════════════════
#  SPARKLINE
# ══════════════════════════════════════════════

def interest_sparkline(breakdown):
    """Show how interest earned per year accelerates."""
    yearly_gains = []
    prev = 0
    for entry in breakdown:
        gain = entry["interest"] - prev
        yearly_gains.append(gain)
        prev = entry["interest"]

    bars   = ["▁","▂","▃","▄","▅","▆","▇","█"]
    lo     = min(yearly_gains)
    hi     = max(yearly_gains)
    spread = hi - lo if hi != lo else 1

    line = ""
    for g in yearly_gains:
        idx   = int((g - lo) / spread * (len(bars) - 1))
        line += bars[idx]

    return f"{GREEN}{line}{RESET}  ← interest earned each year (accelerating!)"

# ══════════════════════════════════════════════
#  OPTION 1 — CALCULATOR
# ══════════════════════════════════════════════

def run_calculator(data):
    header("  📐  COMPOUND INTEREST CALCULATOR")
    print(f"  {DIM}All amounts in Indian Rupees (₹){RESET}\n")

    try:
        principal   = float(input("  💰 Principal Amount (₹)                 : "))
        rate_pct    = float(input("  📈 Annual Interest Rate (%)             : "))
        years       = int(input("  📅 Investment Duration (years)          : "))
        monthly_dep = float(input("  ➕ Monthly Deposit (₹/month, 0 if none) : "))
    except ValueError:
        print(f"\n  {RED}❌ Invalid input. Please enter numbers only.{RESET}")
        return

    if principal < 0 or rate_pct < 0 or years <= 0:
        print(f"\n  {RED}❌ Principal and rate must be positive, years > 0.{RESET}")
        return

    rate = rate_pct / 100

    print(f"""
  Compounding Frequency:
  {CYAN}1.{RESET} Annually    {CYAN}2.{RESET} Quarterly
  {CYAN}3.{RESET} Monthly     {CYAN}4.{RESET} Daily
""")
    freq_map    = {"1": 1, "2": 4, "3": 12, "4": 365}
    freq_name   = {"1": "Annually", "2": "Quarterly", "3": "Monthly", "4": "Daily"}
    freq_choice = input("  Choose (1-4): ").strip()
    n           = freq_map.get(freq_choice, 12)
    freq_label  = freq_name.get(freq_choice, "Monthly")

    clear()
    header("  📊  YOUR INVESTMENT REPORT")

    # ── CALCULATIONS ──
    if monthly_dep > 0:
        final, interest, invested = compound_with_monthly_sip(principal, monthly_dep, rate, n, years)
        total_deposited = monthly_dep * years * 12
    else:
        final, interest = compound_interest(principal, rate, n, years)
        invested        = principal
        total_deposited = 0

    breakdown        = yearly_breakdown(principal, rate, n, years)
    growth_pct       = (interest / invested) * 100
    interest_yearly  = round(interest / years, 2)
    interest_monthly = round(interest / (years * 12), 2)

    # ── INPUT SUMMARY (no colour) ──
    print(f"""
  {BOLD}INPUT SUMMARY{RESET}
  ┌──────────────────────────────────────────────────┐
  │  Principal              :  ₹{principal:>15,.2f}             │
  │  Monthly Deposit        :  ₹{monthly_dep:>15,.2f}             │
  │  Total Deposited        :  ₹{total_deposited:>15,.2f}             │
  │  Annual Rate            :  {rate_pct:>15.2f}%            │
  │  Duration               :  {years:>14} years            │
  │  Compounding            :  {freq_label:>15}            │
  └──────────────────────────────────────────────────┘
""")

    # ── RESULTS (colour here) ──
    print(f"""  {BOLD}RESULTS{RESET}
  ┌──────────────────────────────────────────────────┐
  │  Total Amount Invested  :  {YELLOW}₹{invested:>15,.2f}{RESET}             │
  │                                                  │
  │  Avg Interest / Month   :  {MAGENTA}₹{interest_monthly:>15,.2f}{RESET}             │
  │  Avg Interest / Annum   :  {CYAN}₹{interest_yearly:>15,.2f}{RESET}             │
  │  Total Interest Earned  :  {CYAN}₹{interest:>15,.2f}{RESET}             │
  │                                                  │
  │  {GREEN}{BOLD}Final Amount           :  ₹{final:>15,.2f}{RESET}             │
  │  {GREEN}Wealth Growth          :  {growth_pct:>14.1f}%{RESET}             │
  └──────────────────────────────────────────────────┘
""")

    # ── SPARKLINE ──
    print(f"  📈  Interest Acceleration:")
    print(f"  {interest_sparkline(breakdown)}\n")

    # ── BAR CHART ──
    if years <= 30:
        bar_chart(breakdown, principal)
    else:
        sampled = [b for b in breakdown if b["year"] % 5 == 0]
        bar_chart(sampled, principal)

    # ── MONTHLY DEPOSIT BREAKDOWN ──
    if monthly_dep > 0:
        divider()
        print(f"\n  {BOLD}Deposit Contribution Breakdown:{RESET}")
        lump_final, _ = compound_interest(principal, rate, n, years)
        dep_contribution = final - lump_final
        lump_pct = lump_final / final * 100
        dep_pct  = dep_contribution / final * 100
        print(f"  Lump Sum grew to         : {GREEN}₹{lump_final:>12,.2f}{RESET}  ({lump_pct:.1f}%)")
        print(f"  Monthly Deposits grew to : {CYAN}₹{dep_contribution:>12,.2f}{RESET}  ({dep_pct:.1f}%)")
        print(f"  {YELLOW}💡 Even small monthly deposits make a huge difference!{RESET}")

    # ── SAVE ──
    divider()
    save = input("\n  Save this plan? (y/n): ").strip().lower()
    if save == "y":
        plan_name = input("  Name this plan: ").strip()
        plan = {
            "name":        plan_name,
            "principal":   principal,
            "monthly_dep": monthly_dep,
            "rate":        rate_pct,
            "years":       years,
            "freq":        freq_label,
            "final":       final,
            "interest":    interest,
            "date_saved":  datetime.now().strftime("%d %b %Y")
        }
        data["saved_plans"].append(plan)
        save_investments(data)
        print(f"  {GREEN}✅  Plan '{plan_name}' saved!{RESET}")

# ══════════════════════════════════════════════
#  OPTION 2 — GOAL PLANNER
# ══════════════════════════════════════════════

def goal_planner():
    header("  🎯  GOAL-BASED INVESTMENT PLANNER")
    print(f"  {YELLOW}How much do you need to invest to reach your goal?{RESET}\n")

    try:
        goal     = float(input("  🎯 Target Amount (₹)        : "))
        rate_pct = float(input("  📈 Expected Annual Rate (%) : "))
        years    = int(input("  📅 Time Available (years)   : "))
    except ValueError:
        print(f"\n  {RED}❌ Invalid input.{RESET}")
        return

    if goal <= 0 or rate_pct <= 0 or years <= 0:
        print(f"\n  {RED}❌ All values must be positive.{RESET}")
        return

    rate = rate_pct / 100

    # Reverse compound formula: P = A / (1 + r/n)^(n*t)
    required_lump = goal / math.pow(1 + rate / 12, 12 * years)

    # Monthly deposit required
    r_monthly = rate / 12
    periods   = years * 12
    if r_monthly > 0:
        required_monthly = goal * r_monthly / (math.pow(1 + r_monthly, periods) - 1)
    else:
        required_monthly = goal / periods

    total_deposited  = required_monthly * periods
    interest_earned  = goal - total_deposited
    interest_yearly  = round(interest_earned / years, 2)
    interest_monthly = round(interest_earned / periods, 2)

    # ── INPUT (no colour) ──
    print(f"""
  Your Goal              :  ₹{goal:,.2f}
  Rate                   :  {rate_pct}% per year
  Time                   :  {years} years
""")

    # ── OPTIONS & RESULTS (colour here) ──
    print(f"""  {CYAN}{'═'*55}{RESET}
  Option 1 — Invest a lump sum TODAY:
    {GREEN}{BOLD}₹{required_lump:,.2f}{RESET}  →  grows to ₹{goal:,.0f} in {years} yrs

  Option 2 — Invest monthly:
    {CYAN}{BOLD}₹{required_monthly:,.2f} / month{RESET}  →  grows to ₹{goal:,.0f} in {years} yrs
  {CYAN}{'─'*55}{RESET}

  {BOLD}If you go with monthly deposits:{RESET}
  ┌──────────────────────────────────────────────────┐
  │  Total Amount You Deposit :  {YELLOW}₹{total_deposited:>15,.2f}{RESET}             │
  │                                                  │
  │  Avg Interest / Month     :  {MAGENTA}₹{interest_monthly:>15,.2f}{RESET}             │
  │  Avg Interest / Annum     :  {CYAN}₹{interest_yearly:>15,.2f}{RESET}             │
  │  Total Interest Earned    :  {GREEN}₹{interest_earned:>15,.2f}{RESET}             │
  │                                                  │
  │  {GREEN}{BOLD}Final Amount             :  ₹{goal:>15,.2f}{RESET}             │
  └──────────────────────────────────────────────────┘

  {YELLOW}💡 SIP lets you start small and let compounding do the work!{RESET}
  {CYAN}{'═'*55}{RESET}
""")

# ══════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════

def main():
    data = load_investments()

    if data.get("username") == "Investor":
        clear()
        print(f"\n{CYAN}{BOLD}  💰 Welcome to the Investment Simulator!{RESET}\n")
        name = input("  Enter your name: ").strip()
        if name:
            data["username"] = name
        save_investments(data)

    while True:
        clear()
        print(f"""
{CYAN}{BOLD}
 ╔════════════════════════════════════════════════════════╗
 ║    💰  COMPOUND INTEREST INVESTMENT SIMULATOR  💰      ║
 ║         "Money makes money — and that money            ║
 ║          makes more money."  — Benjamin Franklin       ║
 ╚════════════════════════════════════════════════════════╝{RESET}
  {DIM}Welcome, {RESET}{BOLD}{WHITE}{data["username"]}{RESET}

  {GREEN}1.{RESET} 📐  Compound Interest Calculator  (with Monthly Deposit)
  {CYAN}2.{RESET} 🎯  Goal-Based Planner  (find what you need to invest)
  {DIM}3.{RESET} 🚪  Exit
""")
        divider()
        choice = input("  Your choice (1–3): ").strip()

        if   choice == "1": run_calculator(data)
        elif choice == "2": goal_planner()
        elif choice == "3":
            print(f"\n  {GREEN}{BOLD}  Start early. Stay invested. Let compounding work! 🚀{RESET}\n")
            break
        else:
            print(f"  {RED}❌ Invalid choice.{RESET}")

        input(f"\n  {DIM}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
