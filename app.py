import os
import gradio as gr
import json

try:
    from detector import detector
except Exception:
    class StubDetector:
        def detect(self, query, progress=None):
            return {
                "final_answer": "Stub mode active.",
                "explanations_html": "<p>No model loaded.</p>",
                "evidence_snippets": [],
                "verification_log": [],
                "combined_confidence": 0
            }
    detector = StubDetector()


def process_query(query, progress=gr.Progress()):
    if not query:
        return (
            "<div style='color:red'>Please enter something.</div>",
            "",
            "",
            "",
            0
        )

    res = detector.detect(query, progress)

    return (
        f"<div><h3>Answer</h3>{res['final_answer']}</div>",
        res["explanations_html"],
        json.dumps(res["evidence_snippets"], indent=2),
        "\n".join([f"{a} {b}: {c}" for a, b, c in res["verification_log"]]),
        res["combined_confidence"]
    )


def create_ui():
    with gr.Blocks(title="TruthfulAI") as demo:
        gr.Markdown("# TruthfulAI — Real Model Prototype")

        inp = gr.Textbox(label="Input", lines=3)
        btn = gr.Button("Analyze")

        out_html = gr.HTML()
        out_expl = gr.HTML()
        out_snip = gr.Textbox(lines=8)
        out_log = gr.Textbox(lines=8)
        out_conf = gr.Number()

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
        share=False,
        inbrowser=False,     # IMPORTANT
        show_error=True,     # Good for debugging
        max_threads=40       # Prevent idle shutdown
    )
