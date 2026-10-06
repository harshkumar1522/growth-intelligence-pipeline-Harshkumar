
import os
from google import genai


SYSTEM_INSTRUCTION = """
You are a senior data analyst writing for Mamaearth's regional operations
and finance heads.

Write the business narrative using exactly these three labeled sections:

Situation
Complication
Resolution

Every number in the output must come only from the supplied findings.
Do not invent, estimate, calculate, or introduce any additional statistics.
If a number is mentioned, it must appear with the same value in the findings.
Keep the tone concise, factual, and suitable for senior business leaders.
"""


def generate_scr_narrative(findings: dict) -> dict:
    """
    Generate an S-C-R business narrative using the supplied verified findings.

    Returns a structured dictionary on both success and failure.
    """

    user_prompt = f"""
Using ONLY the supplied verified findings below, write a concise business
narrative for Mamaearth's regional operations and finance heads.

Structure the response with exactly these three labeled sections:

Situation
Complication
Resolution

Focus on:
- overall revenue reconciliation,
- the COD return-rate problem,
- the highest-risk customer segment,
- the duplicate-driven revenue reconciliation,
- and the corrected monthly revenue peak.

Do not introduce any number that is not present in the supplied findings.

SUPPLIED FINDINGS:
{findings}
"""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "narrative": None,
            "tokens": {},
            "message": "GEMINI_API_KEY is not configured."
        }

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": 0.0,
                "max_output_tokens": 500,
                "http_options": {
                    "timeout": 30_000
                }
            }
        )

        narrative = response.text

        usage = getattr(response, "usage_metadata", None)

        tokens = {}

        if usage is not None:
            if getattr(usage, "prompt_token_count", None) is not None:
                tokens["prompt_tokens"] = usage.prompt_token_count

            if getattr(usage, "candidates_token_count", None) is not None:
                tokens["output_tokens"] = usage.candidates_token_count

            if getattr(usage, "total_token_count", None) is not None:
                tokens["total_tokens"] = usage.total_token_count

        return {
            "status": "success",
            "narrative": narrative,
            "tokens": tokens,
            "message": None
        }

    except Exception as err:
        return {
            "status": "error",
            "narrative": None,
            "tokens": {},
            "message": str(err)
        }


def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Fully offline deterministic fallback.
    Uses only values supplied in findings.
    """

    cleaned_revenue = findings["cleaned_total_revenue_inr"]
    raw_revenue = findings["raw_total_revenue_inr"]
    duplicate_delta = findings["duplicate_reconciliation_delta_inr"]

    cod_rate = findings["return_rate_by_payment"]["COD"]
    card_rate = findings["return_rate_by_payment"]["CARD"]
    upi_rate = findings["return_rate_by_payment"]["UPI"]

    segment = findings["highest_risk_segment"]
    risk_rate = segment["return_rate_pct"]

    peak_month = findings["true_peak_month"]["month"]
    peak_revenue = findings["true_peak_month"]["revenue_inr"]

    inflated_month = findings["outlier_inflated_month"]["month"]
    inflated_revenue = findings["outlier_inflated_month"]["apparent_revenue_inr"]
    corrected_revenue = findings["outlier_inflated_month"]["corrected_revenue_inr"]

    narrative = f"""Situation

Cleaned order data reports revenue of ₹{cleaned_revenue:,.2f}, compared with
₹{raw_revenue:,.2f} from the raw SQL layer. The reconciliation difference is
₹{duplicate_delta:,.2f}.

Complication

COD has the highest return rate at {cod_rate:.1f}%, compared with {card_rate:.1f}%
for CARD and {upi_rate:.1f}% for UPI. The highest-risk segment is
{segment["payment_method"]} with City Tier {segment["city_tier"]}, at
{risk_rate:.1f}%. The apparent revenue peak in {inflated_month} was
₹{inflated_revenue:,.2f}, but quantity-outlier correction reduces it to
₹{corrected_revenue:,.2f}.

Resolution

The corrected analysis identifies {peak_month} as the true revenue peak at
₹{peak_revenue:,.2f}. Operations and finance should prioritize the COD and
Tier-2 risk segment while using the cleaned revenue figures for decision-making.
"""

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": {},
        "message": "Generated using the fully offline deterministic fallback."
    }
