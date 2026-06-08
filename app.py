"""
Milestone 5b — Gradio web interface for the Unofficial Internship Guide.

Run:
    python app.py
Then open: http://localhost:7860
"""
import gradio as gr
from generate import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="Unofficial Internship Guide") as demo:
    gr.Markdown("## Unofficial Guide: Tech Internship Recruiting")
    gr.Markdown(
        "Ask questions about application timelines, interview formats, "
        "LeetCode prep, resume tips, and offer decisions. "
        "Answers are grounded in real student experiences and career guides."
    )

    question_box = gr.Textbox(
        label="Your question",
        placeholder="e.g. When should I start applying for Big Tech internships?",
        lines=2,
    )
    ask_btn = gr.Button("Ask", variant="primary")

    answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources_box = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    ask_btn.click(handle_query, inputs=question_box, outputs=[answer_box, sources_box])
    question_box.submit(handle_query, inputs=question_box, outputs=[answer_box, sources_box])

demo.launch()
