"""
Prompts for model evaluation

Short names for each task:
1. CLAS = Classification
2. NAME = Naming
3. BBOX = ImageBbox
4. LABE = ImageLabel
5. CAPT = CaptionHL
6. EXPL = Explanation
"""

# Task 1: Classification (CLAS)

RE_TOKENS_CLAS = 50

INSTRUCT_CLAS02 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Answer the question with Yes or No."
)

INSTRUCT_CLAS03 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Answer the question with Yes (i.e., metaphor use is involved) or No (i.e., metaphor use is not involved)."
)

INSTRUCT_CLAS04 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Label the image-and-caption combination as Metaphorical or Non-metaphorical."
)

RE_TOKENS_CLAS_05 = 200

INSTRUCT_CLAS05 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Label the image-and-caption combination as \"Metaphorical\" or \"Not Metaphorical\"."
)


INSTRUCT_CLAS06 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Answer the question with No or Yes."
)

RE_TOKENS_CLAS07 = 300

INSTRUCT_CLAS07 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Think step-by-step and finish your response with \"Answer: X\" where X is either Y (yes, metaphor use is involved) or N (no, metaphor use is not involved)."
)

INSTRUCT_CLAS08 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Label the image-and-caption combination as M (metaphor use is involved) or N (metaphor use is not involved)."
)

INSTRUCT_CLAS09 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Answer the question with True (i.e., metaphor use is involved) or False (i.e., metaphor use is not involved)."
)

INSTRUCT_CLAS10 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Label the image-and-caption combination as T (metaphor use is involved) or F (metaphor use is not involved)."
)

options_CLAS11 = [
    "The humor of the given image-and-caption combination involves metaphor use.",
    "The humor of the given image-and-caption combination does not involve metaphor use."
]

option_a = ""
option_b = ""

INSTRUCT_CLAS11 = (
    "Does the humor of the given image-and-caption combination involve metaphor use? "
    "Choose from the following options:\n"
    f"A. {option_a}\nB. {option_b}\n"
    "Answer the question with A or B."
)


# Task 2: Naming (NAME)

RE_TOKENS_NAME = 50

INSTRUCT_NAME04 = (
    "The humor of the given image-and-caption combination involves metaphor use. "
    "Which conceptual metaphor is used? "
    "Answer the question in \"TARGET DOMAIN IS SOURCE DOMAIN\" format (e.g., \"LOVE IS A JOURNEY\")."
)


# Task 3: ImageBbox (BBOX)

RE_TOKENS_BBOX = 200

INSTRUCT_BBOX02 = (
    "The humor of the given image-and-caption combination involves metaphor use. "
    "Which object in the image is related to the metaphor? "
    "Answer with its label and normalized bounding box coordinates in \"label: [top, left, height, width]\" format."
)


# Task 4: ImageLabel (LABE)

RE_TOKENS_LABE = 10

INSTRUCT_LABE02 = (
    "The humor of the given image-and-caption combination involves metaphor use. "
    "Which object in the image is related to the metaphor? "
    "Answer the question with a single word."
)


# Task 5: CaptionHL (CAPT)

RE_TOKENS_CAPT = 200

INSTRUCT_CAPT02 = (
    "The humor of the given image-and-caption combination involves metaphor use. "
    "Which part of the caption is related to the metaphor? "
    "Surround it with a pair of <i></i> tag."
)


# Task 6: Explanation (EXPL)

RE_TOKENS_EXPL = 200

INSTRUCT_EXPL06 = (
    "How does metaphor use contribute to the humor of the given image-and-caption combination? "
    "Explain in no more than 30 words."
)

