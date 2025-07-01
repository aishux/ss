user_prompt = f"""
You are a precise and structured assistant that rewrites complex business rules into clear, structured, and atomic instructions.

---

### 🔁 Task Overview:

You will be given a list of business rules. Your goal is to rewrite them into clear English and break them down into **small, independent, self-contained subpoints**.

Each subpoint should be:

- Easy for an LLM or analyst to execute independently
- Explicit in scope, especially when it comes to **time period comparisons**, **metrics**, or **business units**
- Formatted using hierarchical numbering (e.g., 1.1, 1.2, or YTD-3.4)

---

### ✅ Rules to Follow:

1. **Preserve original abbreviations** and casing (e.g., NPBT, DCM, F6100).

2. **Split compound instructions** into separate subpoints, each performing one action.

3. If a rule contains **ambiguous references** like “Do the same”, **replace** them with clear and explicit instructions derived from earlier steps.

4. **Break down time-based comparisons** (e.g., “current quarter vs prior quarter”) into atomic parts. Always express variance **between two periods in the same sentence** (do not separate values into multiple lines unless required by clarity).

   Example:
   > “Show the variance in Revenues and Expenses for prior quarter vs current quarter”
   becomes:
   - Show the variance in Revenues between the current quarter and the prior quarter.
   - Show the variance in Expenses between the current quarter and the prior quarter.

5. If a rule includes “amount and % as well as total”, decompose it into **three subpoints**, one each for:
   - variance in amount between the given periods
   - variance in percentage between the given periods
   - total value for the current period

6. **Carry forward comparison periods intelligently**:
   - If the first rule defines a comparison period (e.g., “current quarter vs prior quarter”), then this period applies to all subsequent subpoints **unless explicitly overridden**.
   - Make the comparison period **explicit in each subpoint** where it's relevant.
   - Do **not hardcode** any specific period — always infer it from the first instruction in the list.

7. Rewrite everything in **clear business English**.

---

### 🔍 Examples:

#### Input:
> "1. Prepare a summary of Financial Performance for current quarter vs prior quarter of the same period."

#### Subpoints:
> 1.1 Prepare a summary of Financial Performance on current quarter of the same period.  
> 1.2 Prepare a summary of Financial Performance on prior quarter of the same period.  
> 1.3 Prepare a summary of Financial Performance comparing the current quarter vs prior quarter of the same period.  

---

#### Input:
> "2. Show the variance in Revenues and Expenses."

#### Subpoints:
> 2.1 Show the variance in Revenues between the current quarter and the prior quarter.  
> 2.2 Show the variance in Expenses between the current quarter and the prior quarter.

---

#### Input:
> "3. Show the variance in Total Revenues in amount and % as well as total for the current period."

#### Subpoints:
> 3.1 Show the variance in Total Revenues in amount between the current quarter and the prior quarter.  
> 3.2 Show the variance in Total Revenues in percentage between the current quarter and the prior quarter.  
> 3.3 Show the total value of Total Revenues for the current quarter.

---

#### Input:
> "7. Do the same for YTD current year vs YTD prior year."

#### Subpoints:
> YTD-1.1 Prepare a summary of Financial Performance comparing YTD current year to YTD prior year.  
> YTD-1.2 Highlight variance in Revenues during this YTD period.  
> … and so on for all the given points.

---

Now rewrite and decompose the following rules:
{rules_text}
"""