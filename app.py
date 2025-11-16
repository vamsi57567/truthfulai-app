import os
import gradio as gr
import json

# NOTE: This is a lightweight wrapper extracted from the notebook's Gradio interface.
# It will try to import the heavy components if available; otherwise it runs in "stub mode".
STUB_MODE = True

# Try to import heavy components (sentence-transformers, faiss, etc.). If unavailable, stay in stub mode.
try:
    import faiss
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from rank_bm25 import BM25Okapi
    from openai import OpenAI
    from sklearn.metrics.pairwise import cosine_similarity
    STUB_MODE = False
except Exception as e:
    print("Warning: running in STUB_MODE (missing heavy dependencies).", e)

# Placeholder detection logic when heavy models are unavailable
class HallucinationDetectorStub:
    def __init__(self):
        pass
    def detect(self, query, progress=None):
        # Return a consistent structure the notebook UI expects
        return {
            "final_answer": "This is a stubbed response. Install the required models and set DATA/MODEL paths to enable full functionality.",
            "explanations_html": "<p><b>Stub mode:</b> no models loaded.</p>",
            "evidence_snippets": [],
            "verification_log": [("ℹ️","Mode","Stub mode active - minimal checks")],
            "combined_confidence": 42,
            "has_web_contradiction": False
        }

# Try to import a real HallucinationDetector from a local module (if user provided it)
detector = None
try:
    # If the notebook's detector class has been converted into detector.py in the repo, this will import it.
    from detector import HallucinationDetector
    detector = HallucinationDetector()
    STUB_MODE = False
except Exception:
    detector = HallucinationDetectorStub()

def create_interface():
    def process_query(query, progress=gr.Progress()):
        if not query or not query.strip():
            return ("<div style='padding:12px;color:#ef4444'>Please enter a claim or question.</div>", "", "", [], None)
        results = detector.detect(query, progress)
        html = f\"\"\"<div style='padding:12px'><h3>Answer</h3><div>{results.get('final_answer')}</div></div>\"\"\"
        explanations = results.get('explanations_html', '')
        snippets = results.get('evidence_snippets', [])
        log = results.get('verification_log', [])
        confidence = results.get('combined_confidence', 0)
        return html, explanations, json.dumps(snippets, indent=2), '\\n'.join([f\"{t[0]} {t[1]}: {t[2]}\" for t in log]), confidence

    with gr.Blocks(title="TruthfulAI — Hallucination Detector (Light) - Space Ready") as demo:
        gr.Markdown(\"\"\"# TruthfulAI — Hallucination Detector\n\nLight deploy-ready wrapper. Replace `detector` with the full implementation for production.\"\"\")
        with gr.Row():
            inp = gr.Textbox(placeholder="Enter a claim or question...", label="Input", lines=3)
            run = gr.Button("Check")
        out_html = gr.HTML()
        out_explanations = gr.HTML(label="Explanations")
        out_evidence = gr.Textbox(label="Evidence snippets (JSON)", lines=6)
        out_log = gr.Textbox(label="Verification log", lines=6)
        out_conf = gr.Number(label="Confidence (%)")
        run.click(process_query, inputs=[inp], outputs=[out_html, out_explanations, out_evidence, out_log, out_conf])
    return demo

if __name__ == '__main__':
    demo = create_interface()
    demo.launch(server_name='0.0.0.0', server_port=int(os.environ.get('PORT', 7860)), share=False)
