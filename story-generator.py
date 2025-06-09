import dspy 
from dotenv import load_dotenv
import os
load_dotenv()


# load the LLM model
open_ai = os.getenv("OPENAI_API_KEY")

llm = dspy.LM("openai/gpt-4o-mini", api_key=open_ai)
dspy.configure(lm=llm)

# The test file as a "Fabula de sopo"
test_file = """The Eagle, the Hare, and the Beetle
A hare was being chased by an eagle, and seeing herself lost, she begged a beetle for help, pleading for its assistance.
The beetle asked the eagle to spare his friend. But the eagle, despising the insignificance of the beetle, devoured the hare in his presence.
From then on, seeking revenge, the beetle observed the places where the eagle laid its eggs, and rolling them, knocked them to the ground. Seeing herself driven away from wherever she went, the eagle turned to Zeus asking for a safe place to lay her eggs.
Zeus offered to let her place them in his lap, but the beetle, seeing this escape tactic, made a small ball of dung, flew up and dropped it on Zeus's lap.
Zeus then stood up to shake off that filth, and unknowingly threw the eggs to the ground. That is why since then, eagles do not lay eggs during the season when beetles come out to fly.
Moral: Never despise what seems insignificant, for there is no being so weak that it cannot reach you."""


# Now we are going to create some dspy clases

class ExtractRelevantInformation(dspy.Signature):
    """Extract the relevant information and jey themes about this story"""
    input_text: str = dspy.InputField()
    main_characters = dspy.OutputField(desc="Main characters in the story")
    reasoning: str = dspy.OutputField(desc="Step by step reasoning of the story, what is this bout? why the characters do what they do?")
    moral_of_the_story: str = dspy.OutputField(desc="The moral lesson or teaching (Enseñanza) of the story")
    key_themes: str = dspy.OutputField(desc="Key themes and main characters identified in the story")

        
class StoryCreation(dspy.Signature):
    """Based on the key themes and moral of the story, create an entertaining story"""
    input_text: str = dspy.InputField()
    main_characters : str = dspy.InputField()
    reasoning: str = dspy.InputField()
    key_themes: str = dspy.InputField()
    moral: str = dspy.InputField()
    story: str = dspy.OutputField(desc="Create an entertaining story incorporating the themes and moral. This story should reflect the reasoning on the story and the moral of the story")


class StoryStructure(dspy.Module):
    def __init__(self):
        super().__init__()
        self.extract_relevant_information = dspy.ChainOfThought(ExtractRelevantInformation)
        self.story_creation = dspy.ChainOfThought(StoryCreation)
    def forward(self, input_text):
        # Firts we are extracting information about the initial text, as much detail as posible (the detail is extracted in the first CoT)
        extracted_info = self.extract_relevant_information(
            input_text = input_text
        )

        # Then we are creating the story using the extracted information
        story = self.story_creation(
            input_text = input_text,
            main_characters = extracted_info.main_characters,
            reasoning = extracted_info.reasoning,
            key_themes = extracted_info.key_themes,
            moral = extracted_info.moral_of_the_story,
        )

        return {
            'themes': extracted_info.key_themes,
            'moral': extracted_info.moral_of_the_story,
            'story': story.story,
            'reasoning': extracted_info.reasoning
        }


# Initialize the story generation
generator = StoryStructure()

# Generate the story and return all the components
result = generator(test_file)

def save_story_result(result_dict, filename="story_output.txt"):
    # Create the formatted string
    result_str = ""
    result_str += "\n" + "="*50 + " TEMAS " + "="*50 + "\n"
    
    result_str += "\n" + "="*50 + " MORAL " + "="*50 + "\n"
    result_str += str(result_dict['moral']) + "\n"
    
    result_str += "\n" + "="*50 + " STORY " + "="*50 + "\n"
    result_str += str(result_dict['story']) + "\n"
    
    result_str += "\n" + "="*50 + " REASONING " + "="*50 + "\n"
    result_str += str(result_dict['reasoning']) + "\n"
    result_str += "\n" + "="*120 + "\n"
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result_str)

# Use it like this:
save_story_result(result, "story_output_based_on_another.txt")
