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
4. **Break down time-based comparisons** (e.g., “current quarter vs prior quarter”) into **multiple atomic parts**, including:
   - Showing the metric individually for each time period
   - Then explicitly comparing the metric across the two periods

   For example:
   > “Show the variance in Revenues and Expenses for prior quarter vs current quarter”
   becomes:
   - Show the variance in Revenues for the prior quarter  
   - Show the variance in Revenues for the current quarter  
   - Show the variance in Expenses for the prior quarter  
   - Show the variance in Expenses for the current quarter  
   - Compare Revenues for the current quarter vs the prior quarter  
   - Compare Expenses for the current quarter vs the prior quarter
5. **Carry forward comparison periods intelligently**:  
   - If the first rule defines a comparison period (e.g., “current quarter vs prior quarter”), then this period applies to all subsequent subpoints **unless explicitly overridden**.
   - Make the comparison period **explicit in each subpoint** where it's relevant (e.g., “compare Revenues for the current quarter vs prior quarter”).
   - Do **not hardcode** any specific period — always infer it from the first instruction in the list.
6. Rewrite everything in **clear business English**.

---

### 🔍 Examples:

#### Input:
> "1. Prepare a summary of Financial Performance for current quarter vs prior quarter of the same period."

#### Subpoints:
> 1.1 Prepare a summary of Financial Performance on current quarter of the same period.
> 1.2 Prepare a summary of Financial Performance on prior quarter of the same period.
> 1.2 Prepare a summary of Financial Performance comparing the above points which is summarising Financial Performance on current quarter vs prior quarter of same period. 

---

#### Input:
> "2. Show the variance in Revenues and Expenses."

#### Subpoints:
> 2.1 Show the variance in Revenues over the comparison period defined in the first instruction.  
> 2.2 Show the variance in Expenses over the same comparison period.

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
