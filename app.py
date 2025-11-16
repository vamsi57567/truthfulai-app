import os
import gradio as gr
import json

# Try importing real detector
try:
    from detector import detector
    REAL_MODE = True
except Exception as e:
    print("⚠️ Using stub mode:", e)
    REAL_MODE = False

    class StubDetector:
        def detect(self, query, progress=None):
            return {
                "final_answer": "Stub mode active. Add your OpenAI key + detector.py to enable real AI.",
                "explanations_html": "<p>No real model loaded.</p>",
                "evidence_snippets": [],
                "verification_log": [("info", "mode", "stub mode active")],
                "combined_confidence": 0
            }

    detector = StubDetector()


def process_query(query, progress=gr.Progress()):
    if not query or not query.strip():
        return (
            "<div style='padding:12px;color:#ef4444'>Please enter a claim or question.</div>",
            "",
            "",
            "",
            0
        )

    results = detector.detect(query, progress)

    html = f"""
    <div style='padding:12px'>
        <h3>Answer</h3>
        <div>{results.get('final_answer')}</div>
    </div>
    """

    explanations = results.get("explanations_html", "")
    snippets = json.dumps(results.get("evidence_snippets", []), indent=2)
    log = "\n".join([f"{item[0]} {item[1]}: {item[2]}" for item in results.get("verification_log", [])])
    confidence = results.get("combined_confidence", 0)

    return html, explanations, snippets, log, confidence


def create_ui():
    with gr.Blocks(title="TruthfulAI") as demo:
        gr.Markdown("# TruthfulAI — Real Model Prototype")

        inp = gr.Textbox(label="Input", placeholder="Enter a question or claim...", lines=3)
        btn = gr.Button("Analyze")

        out_html = gr.HTML()
        out_expl = gr.HTML(label="Explanations")
        out_snip = gr.Textbox(label="Evidence Snippets (JSON)", lines=8)
        out_log = gr.Textbox(label="Verification Log", lines=8)
        out_conf = gr.Number(label="Confidence (%)")

        btn.click(
            process_query,
            inputs=[inp],
            outputs=[out_html, out_expl, out_snip, out_log, out_conf]
        )

    return demo


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    create_ui().launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )
