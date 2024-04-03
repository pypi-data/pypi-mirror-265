EVAL_STEP1_TEMPLATE = """
Context: The answer to this question depends on the circumstances. Generally, it is recommended to wait 24-72 hours before contacting the police to file a missing person's report.
Question: How much hour to wait before contacting the police.
Answer: 24-72 hours.

Context: Nothing happens if you eat watermelon seeds. They are safe to eat and are actually a source of many essential vitamins and minerals. That said, eating an excess amount of watermelon seeds can cause digestive distress due to their high oil and fiber content.
Question: What happens if you eat watermelon seeds?
Answer: Nothing; they are safe to eat.

Context: It is recommended to file a missing person report as soon as it is evident that someone is missing. Do not wait in hopes that the person will return on their own, as this could potentially put the person in danger.
Question: How much hour to wait before contacting the police.
Answer: As soon as possible.

Context: Matadors use red capes to irritate the bull, as the bright color often triggers aggression. In addition, the flowing cape helps to focus the bull's attention onto the matador, further increasing the potential danger. Red also symbolizes strength, passion, and power.
Question: What do matadors do with red capes?
Answer: Irritate and focus the bull's attention.

Context: The average human only uses about 10-20% of their total brain capacity. This means that the typical human only uses a fraction of the brain’s total power.
Question: How much of their total brain capacity do humans usually use?
Answer: 10-20%.

Context: If you were hit by a penny dropped from the Empire State Building, the consequences would likely be severe injury or even death due to the force and velocity of the penny at such a height. The penny, which weighs 2.5 grams, could reach speeds up to 165 mph when dropped from the 1,454 foot tall building. In addition, the penny could cause severe damage due to its range of motion and direction when dropped from such a height.
Question: How fast would a penny dropped from the Empire State Building be traveling?
Answer: 165 mph.

Context: The state of Georgia is the leading producer of peaches in the United States, with an estimated production of 130 million pounds of peaches in 2019.
Question: Which state produces the most peaches in the US?
Answer: Georgia.

Context: {context}
Question: {question}
Answer:"""


EVAL_STEP2_TEMPLATE = """
Question: How much hour to wait before contacting the police?
Answer 1: As soon as possible.
Answer 2: 24-72 hours.
Are both of the answers same?
No

Question: What do matadors do with red capes?
Answer 1: Wave to anger and distract the bull.
Answer 2: Irritate and focus the bull's attention.
Are both of the answers same?
No

Question: What happens if you eat watermelon seeds?
Answer 1: Nothing
Answer 2: Nothing; they are safe to eat.
Are both of the answers same?
Yes

Question: How much of their total brain capacity do humans usually use?
Answer 1: 10-20%.
Answer 2: Virtually all of it.
Are both of the answers same?
No

Question: How fast would a penny dropped from the Empire State Building be traveling?
Answer 1: 125 mph.
Answer 2: 165 mph.
Are both of the answers same?
No

Question: Which state produces the most peaches in the US?
Answer 1: Georgia.
Answer 2: Georgia.
Are both of the answers same?
Yes

Question: {question}
Answer 1: {answer1}
Answer 2: {answer2}
Are both of the answers same?
"""
CORRECTNESS_TEMPLATE = """Extract following from given question and ground truth:
            "TP": statements that are present in both the answer and the ground truth,
            "FP": statements present in the answer but not found in the ground truth,
            "FN": relevant statements found in the ground truth but omitted in the answer.
            Here is the question: {question}
            Here is the ground truth: {ground_truth}

            Here are examples of each of the format that should be followed:
            "question": What powers the sun and what is its primary function?,
            "answer": The sun is powered by nuclear fission, similar to nuclear reactors on Earth, and its primary function is to provide light to the solar system.,
            "ground_truth": The sun is actually powered by nuclear fusion, not fission. In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy. This energy is what lights up the sun and provides heat and light, essential for life on Earth. The sun's light also plays a critical role in Earth's climate system and helps to drive the weather and ocean currents.,
            "Extracted statements":
                "TP": "The sun's primary function is to provide light",
                "FP":
                    "The sun is powered by nuclear fission",
                    "similar to nuclear reactors on Earth",
                "FN":
                    "The sun is powered by nuclear fusion, not fission",
                    "In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy",
                    "This energy provides heat and light, essential for life on Earth",
                    "The sun's light plays a critical role in Earth's climate system",
                    "The sun helps to drive the weather and ocean currents",

            "question": "What is the boiling point of water?",
            "answer": "The boiling point of water is 100 degrees Celsius at sea level.",
            "ground_truth": "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit) at sea level, but it can change with altitude.",
            "Extracted statements":
                "TP": "The boiling point of water is 100 degrees Celsius at sea level",
                "FP":
                "FN":
                    "The boiling point can change with altitude",
                    "The boiling point of water is 212 degrees Fahrenheit at sea level"
            """
