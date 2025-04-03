"""
Example code for testing Qwen2-VL-7B-Instruct
on the benchmark Naming task (prompt id NAME04)

To run other tasks, change the value of the following variables:
- INSTRUCTIONS
- LENGTH
- test_id (this is just for saving output data)

This code should work for all prompts in the `prompts.py` file,
except for CLAS11, which asks the model to output A/B in the Classification task.
To try CLAS11, please use a_or_b.py instead.

Prompts for the benchmark tasks:
1. CLAS02 (Classification)
2. NAME04 (Naming)
3. BBOX02 (ImageBbox)
4. LABE02 (ImageLabel)
5. CAPT02 (CaptionHL)
6. EXPL06 (Explanation)
"""


import json, sys
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

# Import prompts from prompts.py
import prompts


query_range = range(940)
# Which prompt/test
INSTRUCTIONS = prompts.INSTRUCT_NAME04
test_id = f"test_NAME04"
# Max new token
LENGTH = prompts.RE_TOKENS_NAME
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
    return output_text[0]


# Query answer for each item
for i in query_range:
    print(f"\n\nTrial {i}")
    re = query_answer(i)
    if re is None:
        print("Skipped")
        continue

    # Save output data
    data[i][test_id] = {"assistant_text": re}
    print(re)
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)
    print("Response written to", fp)
print("Fin.")
