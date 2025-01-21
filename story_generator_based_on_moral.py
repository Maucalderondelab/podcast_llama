import dspy 
from typing import List, Dict, Optional
from dotenv import load_dotenv
from enum import Enum   
import os
load_dotenv()
from datetime import datetime
# Import the dspy modules and CoT Classes
from helper_functions.resoning_helpers import (
    PromptAnalysis, 
    CharacterDevelopment, 
    PlotSctucture, 
    SettingDevelopment, 
    StoryValidator, 
    TitleGeneration, 
    ConflictType, 
    GenreType, 
    ToneType, 
    get_conflict_preferences, 
    get_genre_preferences, 
    get_tone_preferences
)

# load the LLM model
open_ai = os.getenv("OPENAI_API_KEY")

llm = dspy.LM("openai/gpt-4o-mini", api_key=open_ai)
dspy.configure(lm=llm)


# Now we have to create the story generator with all the classes we've created
class StoryGenerator(dspy.Module):
    def __init__(self, conflict_type: ConflictType = None, genre_type: GenreType = None, tone_type: ToneType = None):
        super().__init__()
        self.conflict_type = conflict_type
        self.genre_type = genre_type
        self.tone_type = tone_type

        # Initialize all the Chain Of Thought modules for each state
        self.prompt_analyzer = dspy.ChainOfThought(PromptAnalysis)
        self.character_developer = dspy.ChainOfThought(CharacterDevelopment)
        self.plot_builder = dspy.ChainOfThought(PlotSctucture)
        self.setting_developer = dspy.ChainOfThought(SettingDevelopment)
        self.validator = dspy.ChainOfThought(StoryValidator)
        self.title_generator = dspy.ChainOfThought(TitleGeneration)

        # Create the resoning caputure buffer
        self.reasoning_buffer = []


    def log_reasoning(self, stage: str, content: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.reasoning_buffer.append(f"\n=== {stage} === [{timestamp}]\n{content}\n")
    
    def forward(self, prompt: str):
        # Stage 1: Prompt Analysis
        self.log_reasoning("PROMPT ANALYSIS", f"Input prompt: {prompt}")
        self.log_reasoning("CONFLICT TYPE", f"Using conflict type: {self.conflict_type.value}")
        self.log_reasoning("GENRE TYPE", f"Using genre type: {self.genre_type.value}")
        self.log_reasoning("TONE TYPE", f"Using tone type: {self.tone_type.value}")
    
        prompt_analysis = self.prompt_analyzer(
            prompt=prompt,
            conflict_type_input=self.conflict_type.value,
            genre_type_input=self.genre_type.value,
            tone_type_input=self.tone_type.value
            )
        self.log_reasoning("PROMPT ANALYSIS RESULTS",
            f"Theme: {prompt_analysis.theme}\n"
            f"Genre: {prompt_analysis.genre}\n"
            f"Tone: {prompt_analysis.tone}\n"
            f"Conflict Type: {prompt_analysis.conflict_type}")

        # Stage 2: Character Development
        self.log_reasoning("CHARACTER DEVELOPMENT", "Developing characters based on theme and tone...")
        characters = self.character_developer(
            theme=prompt_analysis.theme,
            tone=prompt_analysis.tone
        )
        self.log_reasoning("CHARACTER RESULTS",
            f"Protagonist: {characters.portagonist}\n"
            f"Motivation: {characters.motivation}\n"
            f"Supporting Characters: {characters.supporting_characters}")

        # Stage 3: Plot Development
        self.log_reasoning("PLOT DEVELOPMENT", "Constructing plot structure...")
        plot = self.plot_builder(
            character_info=characters,
            theme=prompt_analysis.theme,
            genre=prompt_analysis.genre,
            conflict_type=prompt_analysis.conflict_type
        )
        self.log_reasoning("PLOT STRUCTURE",
            f"Exposition: {plot.exposition}\n"
            f"Inciting Incident: {plot.inciting_incident}\n"
            f"Rising Action: {plot.rising_action}\n"
            f"Climax: {plot.climax}\n"
            f"Falling Action: {plot.falling_action}\n"
            f"Resolution: {plot.resolution}")

        # Stage 4: Setting Development
        self.log_reasoning("SETTING DEVELOPMENT", "Creating story setting...")
        setting = self.setting_developer(
            theme=prompt_analysis.theme,
            tone=prompt_analysis.tone,
            character_info=characters
        )
        self.log_reasoning("SETTING DETAILS",
            f"Location: {setting.location}\n"
            f"Atmosphere: {setting.atmosphere}\n"
            f"Significance: {setting.significance}")

        # Stage 5: Validation
        story_elements = {
            "analysis": prompt_analysis,
            "character_development": characters,
            "plot": plot,
            "setting": setting
        }
        validation = self.validator(story_elements=story_elements)
        self.log_reasoning("VALIDATION",
            f"Consistency Check: {validation.consistency_check}\n"
            f"Theme Service: {validation.theme_service}\n"
            f"Character Consistency: {validation.character_consistency}\n"
            f"Suggestions: {validation.suggestions}")

        return {
            "theme": prompt_analysis.theme,
            "characters": characters,
            "plot": plot,
            "setting": setting,
            "validation": validation,
            "reasoning_log": "\n".join(self.reasoning_buffer)
        }

# Excelente! Now we have to do a stroy asemble with all of these pieces

class StoryAssemblySignature(dspy.Signature):
    """Signature for final story assembly"""
    elements = dspy.InputField(desc="Validated story elements")
    story = dspy.OutputField(desc="Complete assembled story")

class StoryAssembler(dspy.Module):
    def __init__(self):
        super().__init__()
        self.story_assembler = dspy.ChainOfThought(StoryAssemblySignature)
        self.title_generator = dspy.ChainOfThought(TitleGeneration)
    
    def forward(self, elements: Dict) -> tuple:
        # Assemble story
        result = self.story_assembler(elements=elements)
        
        # Generate title
        title_result = self.title_generator(
            story=result.story,
            theme=elements["theme"]
        )
        
        return result.story, title_result.title


# Now we create the final function to create this story
def generate_story(prompt: str, conflict_type: ConflictType = None, genre_type: GenreType = None, tone_type: ToneType = None) -> tuple:
    """Main function to generate a complete story and save files"""
    # Create stories directory if it doesn't exist
    os.makedirs("stories", exist_ok=True)

    # Get user preferences
    if conflict_type is None:
        conflict_type = get_conflict_preferences()
    if genre_type is None:
        genre_type = get_genre_preferences()
    if tone_type is None:
        tone_type = get_tone_preferences()

    # Create the story
    generator = StoryGenerator(
                        conflict_type=conflict_type, 
                        genre_type=genre_type, 
                        tone_type=tone_type
    )
    # Ensamble the story
    assembler = StoryAssembler()

    # Generate story elements and get reasoning log
    story_elements = generator(prompt)
    final_story, story_title = assembler(elements=story_elements)
    
    # Create safe filename from title
    safe_title = "".join(c if c.isalnum() or c.isspace() else "_" for c in story_title)
    safe_title = safe_title.replace(" ", "_")
    
    # Save reasoning log
    reasoning_path = f"stories/{safe_title}_reasoning.txt"
    with open(reasoning_path, "w") as f:
        f.write(f"Story Title: {story_title}\n")
        f.write("=" * 50 + "\n")
        f.write(story_elements["reasoning_log"])
    
    # Save final story
    story_path = f"stories/{safe_title}_story.txt"
    with open(story_path, "w") as f:
        f.write(f"Title: {story_title}\n")
        f.write("=" * 50 + "\n\n")
        f.write(final_story)
    
    print(f"\nFiles saved:")
    print(f"- Reasoning: {reasoning_path}")
    print(f"- Story: {story_path}")
    
    return story_title, final_story, story_elements["reasoning_log"]

if __name__ == "__main__":
    # input_text = "Never despise what seems insignificant, for there is no being so weak that it cannot reach you."
    input_text = "Fimbulwinter. Kratos sits in a cave covered with a black fur hide and looks sadly at the fire. He sighs and pulls out an empty sack containing Faye's ashes. He gently strokes the pouch remembering her. Sighing and putting away the pouch, Kratos takes out a knife and a stick from which he makes an arrow. Out of the white mist, Atreus enters the cave with a deer on his shoulders."
    
    title, story, reasoning = generate_story(input_text)
    print(f"\nGenerated Title: {title}")












