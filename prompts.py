def generate_prompt(combined_text):
    """
    Generate a professional DDR (Detailed Diagnostic Report) prompt.
    
    Args:
        combined_text: Combined text from inspection and thermal PDFs
    
    Returns:
        str: Formatted prompt for Gemini API
    """
    prompt = f"""You are a professional civil engineer with 15+ years of experience in building diagnostics and defect analysis.

Your task is to generate a comprehensive Detailed Diagnostic Report (DDR) based on the provided inspection and thermal imaging data.

STRICT RULES - FOLLOW THESE CAREFULLY:
1. Do NOT invent or assume facts not present in the data
2. If information is missing → clearly state "Not Available"
3. If data is conflicting → mention the conflict explicitly
4. Use simple, client-friendly language (avoid jargon)
5. Be structured, clear, and professional
6. Support all claims with specific data from provided documents
7. Provide practical, actionable recommendations
8. Clearly indicate severity levels with justification

OUTPUT FORMAT (MUST FOLLOW EXACTLY):

## 1. Executive Summary
- Brief overview of property condition
- Primary issues identified
- Overall severity assessment

## 2. Property & Assessment Details
- Property Type:
- Assessment Date:
- Inspector/Method:
- Area Assessed:

## 3. Area-wise Observations
### Each Area Should Include:
- **[Area Name]**
  - Location: [Specific location in building]
  - Issue Found: [Specific defect/observation]
  - Severity: [High/Medium/Low with clear reason]
  - Thermal Data: [If applicable, what thermal images show]
  - Visual Inspection: [What was physically observed]

## 4. Probable Root Causes
- Issue #1: [Root cause analysis]
- Issue #2: [Root cause analysis]
- Connection between issues (if any): [Explain relationships]

## 5. Severity Assessment Summary
| Issue | Severity | Reason | Urgency |
|-------|----------|--------|---------|
| Issue 1 | High/Medium/Low | Why? | Immediate/Soon/Routine |
| Issue 2 | High/Medium/Low | Why? | Immediate/Soon/Routine |

## 6. Recommended Actions
### Immediate Actions (if any):
1. [Action with timeframe - days/weeks]
2. [Action with timeframe]

### Short-term Actions (1-3 months):
1. [Action with cost estimate if possible]
2. [Action]

### Long-term Actions (3-12 months):
1. [Action]
2. [Action]

## 7. Preventive Maintenance Recommendations
- [Specific maintenance step]
- [Monitoring requirement]
- [Future inspection schedule]

## 8. Missing or Unclear Information
- [What data would be helpful]
- [What couldn't be determined from current data]
- [Suggested additional assessments]

## 9. Professional Notes
- Methodology used
- Limitations of current assessment
- Areas requiring further investigation
- Compliance with standards (if applicable)

---

### INSPECTION & THERMAL DATA:
{combined_text}

---

Generate the DDR report now following the exact format above. Be thorough and professional."""
    
    return prompt


def generate_summary_prompt(text, focus_area=""):
    """
    Generate a focused summary prompt for specific analysis.
    
    Args:
        text: Content to analyze
        focus_area: Specific area to focus on
    
    Returns:
        str: Formatted prompt for summary
    """
    if focus_area:
        prompt = f"""As a building diagnostics expert, summarize the key issues found in {focus_area}.

Data:
{text}

Provide:
1. Main defect in this area
2. Severity (High/Medium/Low)
3. Likely cause
4. Recommended fix"""
    else:
        prompt = f"""Summarize the main findings from this inspection data in 3-4 bullet points.

Data:
{text}

Focus on:
- Most critical issues
- Areas of concern
- Recommended next steps"""
    
    return prompt


def generate_cost_estimate_prompt(text):
    """
    Generate prompt for cost estimation.
    
    Args:
        text: DDR content with identified issues
    
    Returns:
        str: Formatted prompt for cost analysis
    """
    prompt = f"""Based on the identified defects and recommended repairs below, provide a rough cost estimate breakdown.

Note: Use typical market rates (can vary by region/contractor/timing)
Do NOT provide exact quotes - use ranges (Low/Medium/High)

Issues & Recommendations:
{text}

Provide:
1. Cost breakdown by issue
2. Total estimated repair cost (range)
3. Cost for immediate vs preventive actions
4. Cost estimate confidence level (High/Medium/Low confidence)"""
    
    return prompt
