import math
import os
import json
from datetime import datetime

GREEN, RED, YELLOW, CYAN, WHITE, BOLD, DIM, MAGENTA, RESET = (
    "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[97m", 
    "\033[1m", "\033[2m", "\033[95m", "\033[0m"
)

DATA_FILE = "investments.json"

# --- File Handling ---
def load_investments():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"username": "Investor", "saved_plans": []}

def save_investments(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Display Helpers ---
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider():
    print(f"{DIM}{'─' * 60}{RESET}")

def header(title):
    print(f"\n{CYAN}{BOLD}{'═' * 60}{RESET}")
    print(f"{CYAN}{BOLD}{title.center(60)}{RESET}")
    print(f"{CYAN}{'═' * 60}{RESET}\n")

# --- Core Formulas ---
def compound_interest(principal, rate, n, t):
    amount = principal * math.pow((1 + rate / n), n * t)
    return round(amount, 2), round(amount - principal, 2)

def compound_with_monthly_sip(principal, monthly_sip, rate, n, t):
    lump_amount = principal * math.pow((1 + rate / n), n * t)
    r_monthly = rate / 12
    periods = int(t * 12)
    
    if r_monthly > 0:
        sip_amount = monthly_sip * ((math.pow(1 + r_monthly, periods) - 1) / r_monthly) * (1 + r_monthly)
    else:
        sip_amount = monthly_sip * periods
        
    total = lump_amount + sip_amount
    total_invested = principal + (monthly_sip * periods)
    
    return round(total, 2), round(total - total_invested, 2), round(total_invested, 2)

def yearly_breakdown(principal, rate, n, t):
    breakdown = []
    for year in range(1, int(t) + 1):
        amount, interest = compound_interest(principal, rate, n, year)
        breakdown.append({"year": year, "amount": amount, "interest": interest})
    return breakdown

# --- Charts & Visuals ---
def bar_chart(breakdown):
    max_amount = breakdown[-1]["amount"]
    
    print(f"\n  {BOLD}Year-by-Year Growth Chart{RESET}\n")
    print(f"  {'YEAR':<6} {'AMOUNT':>14}  {'INT/YEAR':>11}  {'INT/MONTH':>11}  GROWTH BAR")
    divider()

    for entry in breakdown:
        pct = entry["amount"] / max_amount
        bar_len = int(pct * 25)
        
        if pct < 0.4:
            color = YELLOW
        elif pct < 0.75:
            color = CYAN
        else:
            color = GREEN
            
        bar = "█" * bar_len + f"{DIM}░{RESET}" * (25 - bar_len)
        
        print(f"  Yr {entry['year']:<3} {BOLD}₹{entry['amount']:>12,.0f}{RESET}  "
              f"{CYAN}₹{entry['interest']:>9,.2f}{RESET}  "
              f"{MAGENTA}₹{entry['interest']/12:>9,.2f}{RESET}  {color}{bar}{RESET}")

def interest_sparkline(breakdown):
    yearly_gains = []
    prev = 0
    
    for entry in breakdown:
        yearly_gains.append(entry["interest"] - prev)
        prev = entry["interest"]

    bars = ["▁","▂","▃","▄","▅","▆","▇","█"]
    lo = min(yearly_gains)
    hi = max(yearly_gains)
    spread = hi - lo if hi != lo else 1

    line = ""
    for g in yearly_gains:
        idx = int((g - lo) / spread * 7)
        line += bars[idx]

    return f"{GREEN}{line}{RESET}  ← interest earned each year (accelerating!)"

# --- Calculator App ---
def run_calculator(data):
    header("  📐  COMPOUND INTEREST CALCULATOR")
    print(f"  {DIM}All amounts in Indian Rupees (₹){RESET}\n")

    try:
        principal = float(input("  💰 Principal Amount (₹)                 : "))
        rate_pct = float(input("  📈 Annual Interest Rate (%)             : "))
        years = int(input("  📅 Investment Duration (years)          : "))
        monthly_dep = float(input("  ➕ Monthly Deposit (₹/month, 0 if none) : "))
    except ValueError:
        print(f"\n  {RED}❌ Invalid input. Please enter numbers only.{RESET}")
        return

    if principal < 0 or rate_pct < 0 or years <= 0:
        print(f"\n  {RED}❌ Principal and rate must be positive, years > 0.{RESET}")
        return

    rate = rate_pct / 100
    
    print(f"\n  Compounding Frequency:")
    print(f"  {CYAN}1.{RESET} Annually    {CYAN}2.{RESET} Quarterly")
    print(f"  {CYAN}3.{RESET} Monthly     {CYAN}4.{RESET} Daily")
    
    freq_map = {"1": (1, "Annually"), "2": (4, "Quarterly"), "3": (12, "Monthly"), "4": (365, "Daily")}
    freq_choice = input("  Choose (1-4): ").strip()
    n, freq_label = freq_map.get(freq_choice, (12, "Monthly"))

    clear()
    header("  📊  YOUR INVESTMENT REPORT")

    if monthly_dep > 0:
        final, interest, invested = compound_with_monthly_sip(principal, monthly_dep, rate, n, years)
        total_deposited = monthly_dep * years * 12
    else:
        final, interest = compound_interest(principal, rate, n, years)
        invested = principal
        total_deposited = 0

    breakdown = yearly_breakdown(principal, rate, n, years)
    
    print(f"\n  {BOLD}INPUT SUMMARY{RESET}")
    print(f"  ┌{'─'*50}┐")
    print(f"  │  Principal              :  ₹{principal:>15,.2f}            │")
    print(f"  │  Monthly Deposit        :  ₹{monthly_dep:>15,.2f}            │")
    print(f"  │  Total Deposited        :  ₹{total_deposited:>15,.2f}            │")
    print(f"  │  Annual Rate            :  {rate_pct:>15.2f}%            │")
    print(f"  │  Duration               :  {years:>14} years            │")
    print(f"  │  Compounding            :  {freq_label:>15}            │")
    print(f"  └{'─'*50}┘")

    print(f"\n  {BOLD}RESULTS{RESET}")
    print(f"  ┌{'─'*50}┐")
    print(f"  │  Total Amount Invested  :  {YELLOW}₹{invested:>15,.2f}{RESET}            │")
    print(f"  │                                                  │")
    print(f"  │  Avg Interest / Month   :  {MAGENTA}₹{interest/(years*12):>15,.2f}{RESET}            │")
    print(f"  │  Avg Interest / Annum   :  {CYAN}₹{interest/years:>15,.2f}{RESET}            │")
    print(f"  │  Total Interest Earned  :  {CYAN}₹{interest:>15,.2f}{RESET}            │")
    print(f"  │                                                  │")
    print(f"  │  {GREEN}{BOLD}Final Amount           :  ₹{final:>15,.2f}{RESET}            │")
    print(f"  │  {GREEN}Wealth Growth          :  {(interest/invested)*100:>14.1f}%{RESET}            │")
    print(f"  └{'─'*50}┘\n")

    print(f"  📈  Interest Acceleration:\n  {interest_sparkline(breakdown)}\n")

    if years <= 30:
        bar_chart(breakdown)
    else:
        bar_chart([b for b in breakdown if b["year"] % 5 == 0])

    if monthly_dep > 0:
        divider()
        print(f"\n  {BOLD}Deposit Contribution Breakdown:{RESET}")
        lump_final, _ = compound_interest(principal, rate, n, years)
        dep_contribution = final - lump_final
        
        print(f"  Lump Sum grew to         : {GREEN}₹{lump_final:>12,.2f}{RESET}  ({(lump_final/final)*100:.1f}%)")
        print(f"  Monthly Deposits grew to : {CYAN}₹{dep_contribution:>12,.2f}{RESET}  ({(dep_contribution/final)*100:.1f}%)")
        print(f"  {YELLOW}💡 Even small monthly deposits make a huge difference!{RESET}")

    divider()
    save_choice = input("\n  Save this plan? (y/n): ").strip().lower()
    if save_choice == "y":
        plan_name = input("  Name this plan: ").strip()
        data["saved_plans"].append({
            "name": plan_name, 
            "principal": principal, 
            "monthly_dep": monthly_dep,
            "rate": rate_pct, 
            "years": years, 
            "freq": freq_label,
            "final": final, 
            "interest": interest, 
            "date_saved": datetime.now().strftime("%d %b %Y")
        })
        save_investments(data)
        print(f"  {GREEN}✅  Plan '{plan_name}' saved!{RESET}")

# --- Goal Planner App ---
def goal_planner():
    header("  🎯  GOAL-BASED INVESTMENT PLANNER")
    print(f"  {YELLOW}How much do you need to invest to reach your goal?{RESET}\n")

    try:
        goal = float(input("  🎯 Target Amount (₹)        : "))
        rate_pct = float(input("  📈 Expected Annual Rate (%) : "))
        years = int(input("  📅 Time Available (years)   : "))
    except ValueError:
        print(f"\n  {RED}❌ Invalid input.{RESET}")
        return

    if goal <= 0 or rate_pct <= 0 or years <= 0:
        print(f"\n  {RED}❌ All values must be positive.{RESET}")
        return

    rate = rate_pct / 100
    r_monthly = rate / 12
    periods = years * 12

    required_lump = goal / math.pow(1 + r_monthly, periods)
    
    if r_monthly > 0:
        required_monthly = goal * r_monthly / (math.pow(1 + r_monthly, periods) - 1)
    else:
        required_monthly = goal / periods

    total_deposited = required_monthly * periods
    interest_earned = goal - total_deposited

    print(f"\n  Your Goal              :  ₹{goal:,.2f}")
    print(f"  Rate                   :  {rate_pct}% per year")
    print(f"  Time                   :  {years} years\n")

    print(f"  {CYAN}{'═'*55}{RESET}")
    print(f"  Option 1 — Invest a lump sum TODAY:")
    print(f"    {GREEN}{BOLD}₹{required_lump:,.2f}{RESET}  →  grows to ₹{goal:,.0f} in {years} yrs\n")
    print(f"  Option 2 — Invest monthly:")
    print(f"    {CYAN}{BOLD}₹{required_monthly:,.2f} / month{RESET}  →  grows to ₹{goal:,.0f} in {years} yrs")
    print(f"  {CYAN}{'─'*55}{RESET}\n")

    print(f"  {BOLD}If you go with monthly deposits:{RESET}")
    print(f"  ┌{'─'*50}┐")
    print(f"  │  Total Amount You Deposit :  {YELLOW}₹{total_deposited:>15,.2f}{RESET}            │")
    print(f"  │                                                  │")
    print(f"  │  Avg Interest / Month     :  {MAGENTA}₹{interest_earned/periods:>15,.2f}{RESET}            │")
    print(f"  │  Avg Interest / Annum     :  {CYAN}₹{interest_earned/years:>15,.2f}{RESET}            │")
    print(f"  │  Total Interest Earned    :  {GREEN}₹{interest_earned:>15,.2f}{RESET}            │")
    print(f"  │                                                  │")
    print(f"  │  {GREEN}{BOLD}Final Amount             :  ₹{goal:>15,.2f}{RESET}            │")
    print(f"  └{'─'*50}┘\n")
    print(f"  {YELLOW}💡 SIP lets you start small and let compounding do the work!{RESET}")
    print(f"  {CYAN}{'═'*55}{RESET}\n")

# --- Main Menu ---
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
        print(f"\n{CYAN}{BOLD}")
        print(f"  ╔{'═'*56}╗")
        print(f"  ║    💰  COMPOUND INTEREST INVESTMENT SIMULATOR  💰      ║")
        print(f"  ║        \"Money makes money — and that money             ║")
        print(f"  ║         makes more money.\"  — Benjamin Franklin        ║")
        print(f"  ╚{'═'*56}╝{RESET}")
        print(f"   {DIM}Welcome, {RESET}{BOLD}{WHITE}{data['username']}{RESET}\n")
        
        print(f"   {GREEN}1.{RESET} 📐  Compound Interest Calculator")
        print(f"   {CYAN}2.{RESET} 🎯  Goal-Based Planner")
        print(f"   {DIM}3.{RESET} 🚪  Exit\n")
        divider()
        
        choice = input("  Your choice (1–3): ").strip()

        if choice == "1":
            run_calculator(data)
        elif choice == "2":
            goal_planner()
        elif choice == "3":
            print(f"\n  {GREEN}{BOLD}  Start early. Stay invested. Let compounding work! 🚀{RESET}\n")
            break
        else:
            print(f"  {RED}❌ Invalid choice.{RESET}")

        input(f"\n  {DIM}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
