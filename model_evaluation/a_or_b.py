"""
Example code for testing Qwen2-VL-7B-Instruct
on a variation of the benchmark Classification task
that asks the model to output A/B as answer (prompt id CLAS11)
"""


import json, sys, random
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info


# Import prompts from prompts.py
import prompts


query_range = range(940)
# Which prompt/test
options = prompts.options_CLAS11
test_id = f"test_CLAS11"
# Max new token
LENGTH = prompts.RE_TOKENS_CLAS
# Which model
endpoint = "Qwen/Qwen2-VL-7B-Instruct"
images_dir = "../images"
fp = "test_set.json"


# Load test set
# Output data will be written to the same file
with open(fp, "r") as f:
    data = json.load(f)
print("Test set read from", fp)

# Load model and processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    endpoint,
    torch_dtype="auto",
    device_map="auto"
)
processor = AutoProcessor.from_pretrained(endpoint)
print("Testing model", endpoint)


def query_answer(i):
    item = data[i]
    # Only the Classification task uses non-metaphorical items
    if "CLAS" not in test_id and item["is_met"] == "No":
        return None

    # Shuffle options and format instructions
    option_a, option_b = random.sample(options, 2)
    if "involves" in option_a:
        yes = "A"
    else:
        yes = "B"

    INSTRUCTIONS = (
        "Does the humor of the given image-and-caption combination involve metaphor use? "
        "Choose from the following options:\n"
        f"A. {option_a}\nB. {option_b}\n"
        "Answer the question with A or B."
    )

    image_number = item["contest_number"]
    user_text = f"Caption: {item['caption']}\n\n{INSTRUCTIONS}"
    print(f"{image_number}.jpeg")

    # Format prompt
    image_path = f"{images_dir}/{image_number}.jpeg"
    conversation = [
        {
          "role": "user",
          "content": [
              {"type": "image", "image": image_path,},
              {"type": "text", "text": user_text}
            ],
        },
    ]
    prompt = processor.apply_chat_template(
        conversation,
        tokenize=False,
        add_generation_prompt=True
    )
    print(prompt)

    image_inputs, video_inputs = process_vision_info(conversation)
    inputs = processor(
        text=[prompt],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=LENGTH)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
    return {"assistant_text": output_text[0], "yes_option": yes}


# Query answer for each item
for i in query_range:
    print(f"\n\nTrial {i}")
    re = query_answer(i)
    if re is None:
        print("Skipped")
        continue

    # Save output data
    data[i][test_id] = re
    print(re["assistant_text"])
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)
    print("Response written to", fp)
print("Fin.")
