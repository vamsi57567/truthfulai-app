import os
from openai import OpenAI

# Load API key
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


class Detector:
    def detect(self, query, progress=None):
        if not query or not query.strip():
            return {
                "final_answer": "No input provided.",
                "explanations_html": "",
                "evidence_snippets": [],
                "verification_log": [],
                "combined_confidence": 0
            }

        if not api_key:
            return {
                "final_answer": "ERROR: Missing OPENAI_API_KEY in Railway variables.",
                "explanations_html": "<p>Add your API key in Railway → Variables.</p>",
                "evidence_snippets": [],
                "verification_log": [("error", "auth", "No API key found")],
                "combined_confidence": 0
            }

        # Call OpenAI Responses API correctly
        try:
            resp = client.responses.create(
                model="o3-mini",
                input=f"Analyze this claim: {query}"
            )

            # Extract generated text
            answer = resp.output[0].content[0].text

        except Exception as e:
            return {
                "final_answer": f"MODEL ERROR: {str(e)}",
                "explanations_html": "<p>Model failed to generate output.</p>",
                "evidence_snippets": [],
                "verification_log": [("error", "exception", str(e))],
                "combined_confidence": 0
            }

        return {
            "final_answer": answer,
            "explanations_html": f"<p>{answer}</p>",
            "evidence_snippets": [],
            "verification_log": [("info", "model", "o3-mini used")],
            "combined_confidence": 90,
        }


detector = Detector()
