from langchain_huggingface import (
    HuggingFacePipeline,
    ChatHuggingFace,
)

# -------------------------------------------------------
# Local Hugging Face Model
# -------------------------------------------------------

MODEL_ID = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

# -------------------------------------------------------
# Create Hugging Face Pipeline
# -------------------------------------------------------

llm = HuggingFacePipeline.from_model_id(
    model_id=MODEL_ID,
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 256,
        "do_sample": False,
        "return_full_text": False,
    },
)

# -------------------------------------------------------
# Wrap as Chat Model
# -------------------------------------------------------

chat_model = ChatHuggingFace(llm=llm)