import dspy 
from typing import List, Dict, Optional
from dotenv import load_dotenv
from enum import Enum   
import os
load_dotenv()
from datetime import datetime

# load the LLM model
open_ai = os.getenv("OPENAI_API_KEY")

llm = dspy.LM("openai/gpt-4o-mini", api_key=open_ai)
dspy.configure(lm=llm)


# Now we are going to create some dspy clases. For this purpose we are going to need that our story consist of the 5 elements

# we create a class for the conflict type
class ConflictType(Enum):
   # CHARACTER_VS_CHARACTER = "Character vs Character"
   # CHARACTER_VS_NATURE = "Character vs Nature"
   # CHARACTER_VS_SOCIETY = "Character vs Society"
    CHARACTER_VS_WORLD = "Character vs World"
   # CHARACTER_VS_SELF = "Character vs Self"

# We make a prompt analysis with a sequence of reasoning
class PromptAnalysis(dspy.Signature):
    """Analyze the initial story promp to extract important elements"""
    # Inputs
    prompt = dspy.InputField()

    # Outputs
    theme = dspy.OutputField(desc="Main theme or the moral of the story")
    genre = dspy.OutputField(desc="Genre of the story")
    tone = dspy.OutputField(desc="Tone of the story, keep a serious and reflective tone")
    conflict_type = dspy.OutputField(desc="Conflict type of the story")

# Create a character development 
class CharacterDevelopment(dspy.Signature):
    """Develop the main character and supporting characters"""
    # Inputs
    theme = dspy.InputField()
    tone = dspy.InputField()

    # Outputs
    portagonist = dspy.OutputField(desc="Detailed description of the main character")
    motivation = dspy.OutputField(desc="Character's primary motivation")
    supporting_characters = dspy.OutputField(desc="Detailed description of supporting characters")

# Create the plot structure
class PlotSctucture(dspy.Signature):
    """Create a detailed plot structure"""
    # Inputs
    character_info = dspy.InputField()
    theme = dspy.InputField()
    genre = dspy.InputField()
    conflict_type = dspy.InputField()

    # Outputs
    exposition = dspy.OutputField(desc="Story setup and background")
    inciting_incident = dspy.OutputField(desc="Event that starts the main conflict")
    rising_action = dspy.OutputField(desc="Series of events building tension")
    climax = dspy.OutputField(desc="Peak of conflict and tension")
    falling_action = dspy.OutputField(desc="Events following climax")
    resolution = dspy.OutputField(desc="How story concludes")

# Setting the development of the story
class SettingDevelopment(dspy.Signature):
    """Create story setting that supports theme and characters"""
    # Inputs
    theme = dspy.InputField()
    tone = dspy.InputField()
    character_info = dspy.InputField()

    # Outputs
    location = dspy.OutputField(desc="Setting of the story")
    atmosphere = dspy.OutputField(desc="Enviriomental and emotional atmosphere of the story")
    significance = dspy.OutputField(desc="Significance of the setting for the story")

# Create a story validador Signature
class StoryValidator(dspy.Signature):
    """Validate story elements for consistency and theme service"""
    # Inputs
    story_elements = dspy.InputField(desc="All story elements to validate")

    # Outputs
    consistency_check = dspy.OutputField(desc="Check for plot holes and inconsistencies")
    theme_service = dspy.OutputField(desc="How elements support the theme")
    character_consistency = dspy.OutputField(desc="Character behavior consistency")
    suggestions = dspy.OutputField(desc="Improvement suggestions")

class TitleGeneration(dspy.Signature):
    """Generates a consistent title for the story"""
    # Inputs
    story = dspy.InputField()
    theme = dspy.InputField()

    # Outputs
    title = dspy.OutputField(desc="Concise title (6-9 words) that captures story essence")

# Now we have to create the story generator with all the classes we've created
class StoryGenerator(dspy.Module):
    def __init__(self):
        super().__init__()

        # Initialize all the Chain Of Thought modules for each state
        self.prompt_analyzer = dspy.ChainOfThought(PromptAnalysis)
        self.character_developer = dspy.ChainOfThought(CharacterDevelopment)
        self.plot_builder = dspy.ChainOfThought(PlotSctucture)
        self.setting_developer = dspy.ChainOfThought(SettingDevelopment)
        self.validator = dspy.ChainOfThought(StoryValidator)
        self.title_generator = dspy.ChainOfThought(TitleGeneration)

        # Create the resoning caputure buffer
        self.reasoning_buffer = []

        # Custom rationales for each stage
        self.character_rationale = dspy.OutputField(
            prefix="Reasoning: Let's develop our character by considering",
            desc="${create compelling characters}. We..."
        )

        self.plot_rationale = dspy.OutputField(
            prefix="Reasoning: Let's structure our plot by",
            desc="${build rising action and conflict}. We..."
        )
    
    def log_reasoning(self, stage: str, content: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.reasoning_buffer.append(f"\n=== {stage} === [{timestamp}]\n{content}\n")
    
    def forward(self, prompt: str):
        # Stage 1: Prompt Analysis
        self.log_reasoning("PROMPT ANALYSIS", f"Input prompt: {prompt}")
        prompt_analysis = self.prompt_analyzer(prompt=prompt)
        self.log_reasoning("ANALYSIS RESULTS", 
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
def generate_story(prompt: str) -> tuple:
    """Main function to generate a complete story and save files"""
    # Create stories directory if it doesn't exist
    os.makedirs("stories", exist_ok=True)
    
    generator = StoryGenerator()
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
