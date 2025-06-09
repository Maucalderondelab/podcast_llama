import streamlit as st
import dspy
import os

from typing import List, Dict, Optional
from dotenv import load_dotenv
from datetime import datetime

# Imports from other files
from helper_functions.reasoning_functions import (
    PromptAnalysis, 
    CharacterDevelopment, 
    PlotSctucture, 
    SettingDevelopment, 
    StoryValidator, 
    TitleGeneration, 
    ConflictType, 
    GenreType, 
    ToneType, 
    StoryAssemblySignature,
    get_conflict_preferences, 
    get_genre_preferences, 
    get_tone_preferences
)

# Import the API key
load_dotenv()
open_ai = os.getenv("OPENAI_API_KEY")
llm = dspy.LM("openai/gpt-4o-mini", api_key=open_ai)
dspy.configure(lm=llm)

# Create the CoT with the classes from the reasonig file
class StoryGenerator(dspy.Module):
    def __init__(
        self,
        conflict_type: ConflictType = None,
        genre_type: GenreType = None,
        tone_type: ToneType = None
    ):
        super().__init__()
        self.conflict_type = conflict_type
        self.genre_type = genre_type
        self.tone_type = tone_type
        
        self.prompt_analyzer = dspy.ChainOfThought(PromptAnalysis)
        self.character_developer = dspy.ChainOfThought(CharacterDevelopment)
        self.plot_structure = dspy.ChainOfThought(PlotSctucture)
        self.setting_developer = dspy.ChainOfThought(SettingDevelopment)
        self.validator = dspy.ChainOfThought(StoryValidator)

        self.reasoning_buffer = []
    def log_reasoning(self, stage: str, content: str):
        self.reasoning_buffer.append(f"\n🟢 {stage}\n{content}")

    def forward(self, prompt: str):
        
    # Step 1: Create the prompt analyzer for our model
        # Make the log reasoning
        self.log_reasoning("INPUT PROMPT", prompt)
        self.log_reasoning("CONFLICT TYPE", self.conflict_type.value)
        self.log_reasoning("GENRE TYPE", self.genre_type.value)
        self.log_reasoning("TONE TYPE", self.tone_type.value)
        
        # Run the prompt analizer
        prompt_analysis = self.prompt_analyzer(
            prompt=prompt,
            conflict_type_input=self.conflict_type.value,
            genre_type_input=self.genre_type.value,
            tone_type_input=self.tone_type.value
            )
        self.log_reasoning(
            "PROMPT ANALYSIS RESULTS",
            f"**Theme**: {prompt_analysis.theme}\n"                   
        )

    # Step 2: Create the character development for our model
        # Run the character development 
        characters = self.character_developer(
            theme = prompt_analysis.theme,
            tone = self.tone_type.value
        )
        
        self.log_reasoning(
            "CHARACTER DEVELOPMENT RESULTS",
            f"**Protagonist**: {characters.protagonist}\n"
            f"**Motivation**: {characters.motivation}\n"
            f"**Supporting Characters**: {characters.supporting_characters}"
        )
    # Step 3: Setting the ambient 
        # Run the setting development
        setting = self.setting_developer(
            prompt = prompt,
            theme = prompt_analysis.theme,
            tone = self.tone_type,
            character_info = characters
        )

        self.log_reasoning("SETTING DEVELOPMENT RESULTS",
            f"**Setting**: {setting.location}\n"
            f"**Atmosphere**: {setting.atmosphere}\n"
            f"**Significance**: {setting.significance}")

    # Step 4: Create the plor of our stroy
        # Run the plot structure
        plot = self.plot_structure(
            character_info = characters,
            theme = prompt_analysis.theme,
            genre = self.genre_type,
            conflict = self.conflict_type,
            setting = setting
        )

        self.log_reasoning("PLOT STRUCTURE",
            f"**Exposition**: {plot.exposition}\n"
            f"**Inciting Incident**: {plot.inciting_incident}\n"
            f"**Rising Action**: {plot.rising_action}\n"
            f"**Climax**: {plot.climax}\n"
            f"**Falling Action**: {plot.falling_action}\n"
            f"**Resolution**: {plot.resolution}")

    # Step 5: Validate the story
        # Run the validation gathered into a single variable called story
        story_elements = {
            "analysis": prompt_analysis,
            "character_development": characters,
            "plot": plot,
            "setting": setting
        }
        validation = self.validator(story_elements=story_elements)
        self.log_reasoning("VALIDATION",
            f"**Consistency Check*: {validation.consistency_check}\n"
            f"**Theme Service**: {validation.theme_service}\n"
            f"**Character Consistency**: {validation.character_consistency}\n"
            f"**Suggestions**: {validation.suggestions}")

        return {
            "theme": prompt_analysis.theme,
            "characters": characters,
            "plot": plot,
            "setting": setting,
            "validation": validation,
            "reasoning_log": "\n".join(self.reasoning_buffer)
        }

        
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

# Define the story generation function
def generate_story(prompt: str, conflict_type, genre_type, tone_type):
    generator = StoryGenerator(
            conflict_type=conflict_type, 
            genre_type=genre_type, 
            tone_type=tone_type
    )
    assembler = StoryAssembler()

    # Generate story elements and get reasoning log
    story_elements = generator(prompt)
    final_story, story_title = assembler(elements=story_elements)

    return story_title, final_story, story_elements["reasoning_log"]

def main():
    
    # Set the configuration of the page
    st.set_page_config(
        page_title="Story generator",
        page_icon="📖",
        layout="wide"
    )

    st.title('Story generator')
    
    # make the introduction
    st.markdown("""
    Welcome to the Story Generator! This tool helps you create unique stories using AI.
    Just follow these simple steps:
    1. Enter your story prompt or idea
    2. Select the type of conflict
    3. Choose your preferred genre
    4. Click generate and watch your story come to life!
    """)

    # Input section
    st.subheader("Story Details")
    
    # Text input for story prompt
    prompt = st.text_area(
        "Enter your story prompt or idea:",
        height=100,
        placeholder="Enter your story idea here..."
    )
    

    col1, col2, col3 = st.columns(3)

    with col1:
        conflict_type = st.selectbox(
            "Select a conflict type:",
            list(ConflictType),
            format_func=lambda x: x.value
        )

    with col2:
        genre_type = st.selectbox(
            "Select a genre type:",
            list(GenreType),
            format_func=lambda x: x.value
        )
    with col3:
        tone_type = st.selectbox(
            "Select a tne type:",
            list(ToneType),
            format_func=lambda x: x.value
        )

    # Generate button
    if st.button("Generate Story", type="primary"):
        if not prompt:
            st.error("Please enter a story prompt first!")
            return

        try:
            with st.spinner("Generating your story..."):
                story_title, final_story, reasoning = generate_story(
                    prompt, 
                    conflict_type=conflict_type,
                    genre_type=genre_type,
                    tone_type=tone_type
                )

            # Create tabs for story and reasoning
            story_tab, reasoning_tab = st.tabs(["Generated Story", "Story Reasoning"])

            with story_tab:
                st.subheader(story_title)
                st.write(final_story)
                
                # Add download buttons for the story
                st.download_button(
                    label="Download Story",
                    data=f"Title: {story_title}\n{'=' * 50}\n\n{final_story}",
                    file_name=f"{story_title.replace(' ', '_')}_story.txt",
                    mime="text/plain"
                )

            with reasoning_tab:
                st.subheader("Story Generation Process")
                st.text(reasoning)
                
                # Add download button for reasoning
                st.download_button(
                    label="Download Reasoning",
                    data=f"Story Title: {story_title}\n{'=' * 50}\n{reasoning}",
                    file_name=f"{story_title.replace(' ', '_')}_reasoning.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred while generating the story: {str(e)}")
if __name__ == "__main__":
    main()
