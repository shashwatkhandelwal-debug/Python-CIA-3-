# Project Report: Compound Interest & SIP Investment Simulator

**Institution:** Christ University, Delhi-NCR  
**Course:** [Insert Course Name, e.g., Financial Management / Business Computing]  
**Submitted By:** [Your Name]  
**Registration Number:** [Your Roll/Reg Number]  
**Date:** [Insert Date]  

---

## 1. Project Objective
The objective of this project is to apply programming logic to core financial concepts. By building a terminal-based Python application, this project demonstrates the "Time Value of Money" through compound interest and Systematic Investment Plans (SIP). It provides an interactive way to visualize wealth growth and reverse-engineer financial goals.

## 2. Key Features
* **Compound Interest Calculator:** Calculates future wealth based on the principal amount, expected annual return, investment duration, and optional monthly SIP contributions.
* **Goal-Based Financial Planner:** Allows the user to input a target corpus and timeline, automatically calculating the required lump-sum or monthly investment needed to reach that goal.
* **Visual Data Representation:** Generates a dynamic, color-coded ASCII "Year-by-Year Growth Chart" and a sparkline directly in the terminal to visualize how interest accelerates over time.
* **Data Persistence:** Utilizes Python's `json` library to locally save and retrieve the user's customized financial plans.

## 3. Financial Formulas Used
The core logic of the application relies on the following standard financial formulas:
* **Standard Compound Interest:** $A = P \times (1 + \frac{r}{n})^{nt}$
* **Future Value of a Series (SIP):** $FV = P \times \left[ \frac{(1 + i)^n - 1}{i} \right] \times (1 + i)$

## 4. System Requirements & Execution
This application is designed to be lightweight and accessible.
* **Requirements:** Python 3.6 or higher. No external libraries or standard modules (like `numpy` or `pandas`) are required; the project strictly utilizes built-in libraries (`math`, `os`, `json`, `datetime`).
* **Execution:** 1. Open a terminal or command prompt.
  2. Ensure `investments.json` is in the same directory (the script will create one automatically if it does not exist).
  3. Run the script using the command: `python [your_filename].py`

## 5. Code Structure & Modules
* `load_investments()` / `save_investments()`: Handles file I/O for data persistence.
* `compound_with_monthly_sip()`: The core algorithmic engine for processing the financial mathematics.
* `bar_chart()` / `interest_sparkline()`: Transforms the numerical breakdown into visual terminal outputs using string multiplication and ANSI color codes.
* `main()`: The primary execution loop handling the user interface and menu navigation.

## 6. Conclusion
This project successfully bridges the gap between basic coding and practical business applications. It highlights how iterative loops, mathematical functions, and conditional logic can be combined to build a functional financial tool that aids in investment decision-making.
