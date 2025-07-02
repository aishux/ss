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

3. If a rule contains ambiguous references like “Do the same” or “Repeat the same analysis”, **resolve them explicitly**:
   - If the rule references an earlier point, infer its structure and **reconstruct** it with the new subject.
   - Example: "Do the same Revenue analysis for Global Markets" should follow the same structure as “Revenue analysis for Global Banking”, but adapted to Global Markets.
   - Do **not leave any dependency implicit** — fully expand it.

4. **Break down time-based comparisons** (e.g., “current quarter vs prior quarter”) into atomic parts. Always express **variance** between two periods in the **same sentence**, rather than splitting them into separate lines.

   Example:  
   > “Show the variance in Revenues and Expenses for prior quarter vs current quarter”  
   becomes:  
   - Show the variance in Revenues between the current quarter and the prior quarter.  
   - Show the variance in Expenses between the current quarter and the prior quarter.

5. If a rule includes “amount and % as well as total”, decompose it into **three subpoints**, each for:
   - variance in amount (between the periods)
   - variance in percentage (between the periods)
   - total value for the current period

6. If a rule at the end (e.g., Rule 7) says to repeat all previous steps for a new time period (e.g., YTD instead of QTD):
   - **Do not re-list all prior rules separately.**
   - Instead, for each relevant subpoint from earlier, include **both QTD and YTD** variants.
   - Clearly specify time periods in each subpoint (e.g., “for the current quarter vs prior quarter” and “for YTD current year vs YTD prior year”).
   - Integrate these into the main instruction list rather than duplicating rules.

7. Rewrite everything in **clear, formal business English**.

---

### 🔍 Examples:

#### Input:
> "1. Prepare a summary of Financial Performance for current quarter vs prior quarter of the same period."  
> "7. Do the same for YTD current year vs YTD prior year."

#### Subpoints:
> 1.1 Prepare a summary of Financial Performance for the current quarter vs prior quarter of the same period.  
> 1.2 Prepare a summary of Financial Performance for YTD current year vs YTD prior year.  
> 1.3 Highlight the variance in Revenues between the current quarter and the prior quarter.  
> 1.4 Highlight the variance in Revenues between YTD current year and YTD prior year.  
> 1.5 Highlight the variance in Expenses between the current quarter and the prior quarter.  
> 1.6 Highlight the variance in Expenses between YTD current year and YTD prior year.  

---

#### Input:
> "3. Show the variance in Total Revenues in amount and % as well as total for the current period."

#### Subpoints:
> 3.1 Show the variance in Total Revenues in amount between the current quarter and the prior quarter.  
> 3.2 Show the variance in Total Revenues in percentage between the current quarter and the prior quarter.  
> 3.3 Show the total value of Total Revenues for the current quarter.  
> 3.4 Show the variance in Total Revenues in amount between YTD current year and YTD prior year.  
> 3.5 Show the variance in Total Revenues in percentage between YTD current year and YTD prior year.  
> 3.6 Show the total value of Total Revenues for YTD current year.

---

#### Input:
> "4. Do the same Revenue analysis but for Global Markets."

#### Subpoints:
> 4.1 Prepare a headline section for Global Markets total Revenues.  
> 4.2 Show the variance in Revenues in amount between the current quarter and the prior quarter.  
> 4.3 Show the variance in Revenues in percentage between the current quarter and the prior quarter.  
> 4.4 Show the total value of Revenues for the current quarter.  
> 4.5 Show the variance in Revenues in amount between YTD current year and YTD prior year.  
> 4.6 Show the variance in Revenues in percentage between YTD current year and YTD prior year.  
> 4.7 Show the total value of Revenues for YTD current year.  
> 4.8 Identify the Business Areas in Global Markets driving the variances.  
> 4.9 Include analysis for Execution Services, Derivatives & Solutions, and Financing.  
> 4.10 Use the hierarchy F6100 to structure the Equities and FX/Credit section similarly.

---

Now rewrite and decompose the following rules:
{rules_text}
"""
