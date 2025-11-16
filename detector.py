import os
from openai import OpenAI

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
            # Use the official ChatCompletion API
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",   # o3-mini is not available in Python SDK
                messages=[
                    {
                        "role": "system",
                        "content": "You are a factual verification assistant."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this claim factually: {query}"
                    }
                ]
            )

            answer = resp.choices[0].message["content"]

            return {
                "final_answer": answer,
                "explanations_html": f"<p>{answer}</p>",
                "evidence_snippets": [],
                "verification_log": [("info", "model", "gpt-4.1-mini used")],
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
