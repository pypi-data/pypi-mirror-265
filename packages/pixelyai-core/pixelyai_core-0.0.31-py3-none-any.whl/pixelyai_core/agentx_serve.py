import agentx

from .serving.agentx_serve import AgentXServer
from absl.app import flags, run

FLAGS = flags.FLAGS

flags.DEFINE_string(
    "model_name",
    "pixely3b",
    help="AgentX model name"
)

flags.DEFINE_enum(
    "prompt_format",
    enum_values=[
        "llama2",
        "chatml",
        "openchat",
        "zephyr"
    ],
    default="zephyr",
    help="prompt format for model",
)

flags.DEFINE_bool(
    "share",
    False,
    "Share the gradio application"
)


def main(argv):
    max_sequence_length = 4096
    server = AgentXServer(
        engine=agentx.ServeEngine.from_ollama_model(
            FLAGS.model_name,
            sample_config=agentx.SampleParams(
                max_sequence_length=max_sequence_length,
                max_new_tokens=max_sequence_length,
                temperature=0.2,
                top_p=0.95,
                top_k=20,
                mode="Chat"
            ),
            prompter=agentx.PromptTemplates.from_prompt_templates(
                FLAGS.prompt_format,
                "<|endoftext|>",
                "<|endoftext|>"
            )
        ),
    )
    server.build().queue(max_size=8).launch(
        share=FLAGS.share,
        server_name="0.0.0.0",
    )


if __name__ == "__main__":
    run(main)
