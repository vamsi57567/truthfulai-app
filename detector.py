import os
from openai import OpenAI

# Do NOT pass api_key manually — OpenAI SDK auto-loads env vars
client = OpenAI()

class Detector:
    def detect(self, query, progress=None):
        if not query:
            return {
                "final_answer": "No input provided.",
                "explanations_html": "",
                "evidence_snippets": [],
                "verification_log": [],
                "combined_confidence": 0
            }

        try:
            # Call OpenAI reasoning model
            resp = client.responses.create(
                model="o3-mini",
                input=f"Analyze this claim: {query}"
            )

            answer = resp.output_text

            return {
                "final_answer": answer,
                "explanations_html": f"<p>{answer}</p>",
                "evidence_snippets": [],
                "verification_log": [("info", "model", "o3-mini used")],
                "combined_confidence": 90,
            }

        except Exception as e:
            return {
                "final_answer": f"MODEL ERROR: {str(e)}",
                "explanations_html": "",
                "evidence_snippets": [],
                "verification_log": [("error", "exception", str(e))],
                "combined_confidence": 0,
            }

detector = Detector()
