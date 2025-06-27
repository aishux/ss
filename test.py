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

4. **Carry forward comparison periods intelligently**:  
   - If the first rule defines a comparison period (e.g., “current quarter vs prior quarter”), then this period applies to all subsequent subpoints **unless explicitly overridden**.
   - Make the comparison period **explicit in each subpoint** where it's relevant (e.g., “compare Revenues for the current quarter vs prior quarter”).
   - Do **not hardcode** any specific period — always infer it from the first instruction in the list.

5. Rewrite everything in **clear business English**.

6. If a rule says to "compare X for period A vs period B" or "show variance in X and Y for period A vs B", then:
   - Break it down into 4 steps:  
     (a) state X for period A,  
     (b) state X for period B,  
     (c) state Y for period A,  
     (d) state Y for period B  
   - Then include comparisons:  
     (e) compare X across A and B,  
     (f) compare Y across A and B.  
   This ensures both value extraction and comparative analysis are independently actionable.

---

### 🔍 Examples:

#### Input:
> "1. Prepare a summary of Financial Performance for current quarter vs prior quarter of the same period."

#### Subpoints:
> 1.1 Prepare a summary of Financial Performance comparing the current quarter to the prior quarter of the same period.

---

#### Input:
> "2. Show the variance in Revenues and Expenses."

#### Subpoints:
> 2.1 Show the variance in Revenues over the comparison period defined in the first instruction.  
> 2.2 Show the variance in Expenses over the same comparison period.

---

#### Input:
> "3. Show the variance in Revenues and Expenses for prior quarter vs current quarter."

#### Subpoints:
> 3.1 Show the variance in Revenues for the prior quarter.  
> 3.2 Show the variance in Revenues for the current quarter.  
> 3.3 Show the variance in Expenses for the prior quarter.  
> 3.4 Show the variance in Expenses for the current quarter.  
> 3.5 Compare the Revenues for the prior quarter with the Revenues for the current quarter.  
> 3.6 Compare the Expenses for the prior quarter with the Expenses for the current quarter.

---

Now rewrite and decompose the following rules:
{rules_text}
"""
