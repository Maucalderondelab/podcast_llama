
import dspy
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

# we create a class for the conflict type
class ConflictType(Enum):
    CHARACTER_VS_CHARACTER = "Character vs Character"
    CHARACTER_VS_NATURE = "Character vs Nature"
    CHARACTER_VS_SOCIETY = "Character vs Society"
    CHARACTER_VS_WORLD = "Character vs World"
    CHARACTER_VS_SELF = "Character vs Self"
    
    @classmethod
    def list_options(cls):
        return [f"{conflict.name}: {conflict.value}" for conflict in cls]

class GenreType(Enum):
    SCIENCE_FICTION = "Science Fiction"
    ROMANCE = "Romance"
    MYSTERY = "Mystery"
    
    @classmethod
    def list_options(cls):
        return [f"{genre.name}: {genre.value}" for genre in cls]

class ToneType(Enum):
    SERIOUS = "Serious"
    REFLECTIVE = "Reflective"
    HUMOROUS = "Humorous"
    
    @classmethod
    def list_options(cls):
        return [f"{tone.name}: {tone.value}" for tone in cls]

# We make a prompt analysis with a sequence of reasoning
class PromptAnalysis(dspy.Signature):
    """Analyze the initial story promp to extract important elements"""
    # Inputs
    prompt = dspy.InputField()
    conflict_type_input = dspy.InputField()
    genre_type_input = dspy.InputField()
    tone_type_input = dspy.InputField()
    # Outputs
    theme = dspy.OutputField(desc="Analyze the prompt and with the conflict type, genre type and tone. With that information deduce the theme of the story")

# Create a character development 
class CharacterDevelopment(dspy.Signature):
    """Develop the main character and supporting characters. Keep the original characters if there are some."""
    # Inputs
    theme = dspy.InputField()
    tone = dspy.InputField()

    # Outputs
    protagonist = dspy.OutputField(desc="Detailed description of the main character")
    motivation = dspy.OutputField(desc="Character's primary motivation")
    supporting_characters = dspy.OutputField(desc="Detailed description of supporting characters")

# Create the plot structure
class PlotSctucture(dspy.Signature):
    """Create a detailed plot structure"""
    # Inputs
    character_info = dspy.InputField()
    theme = dspy.InputField()
    genre = dspy.InputField()
    conflict = dspy.InputField()
    setting = dspy.InputField()

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
    prompt = dspy.InputField()
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
class StoryAssemblySignature(dspy.Signature):
    """Signature for final story assembly"""
    elements = dspy.InputField(desc="Validated story elements")
    story = dspy.OutputField(desc="Assemble the story and make sure that is coherent with the elements. Also apply the suggestion ")

# Create a function to obtain the user preferences

def get_conflict_preferences():
    print("Select a conflict type:")
    conflict_types = list(ConflictType)

    # Display options
    for i, conflict in enumerate(conflict_types):
        print(f"{i + 1}. {conflict.value}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(conflict_types):
                conflict_types = conflict_types[choice-1]
                print(f"You selected the confict to be : {conflict_types.value}")
                return conflict_types 
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_genre_preferences() -> GenreType:
    print("\nSelect a genre:")
    genre_types = list(GenreType)
    
    # Display options
    for i, genre in enumerate(genre_types, 1):
        print(f"{i}. {genre.value}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of your choice: "))
            if 1 <= choice <= len(genre_types):
                selected_genre = genre_types[choice - 1]
                print(f"You selected the genre to be : {selected_genre.value}")
                return selected_genre
            else:
                print(f"Please enter a number between 1 and {len(genre_types)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_tone_preferences() -> GenreType:
    print("\nSelect a tone of the story:")
    tone_types = list(ToneType)
    
    # Display options
    for i, tone in enumerate(tone_types, 1):
        print(f"{i}. {tone.value}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of your choice: "))
            if 1 <= choice <= len(tone_types):
                selected_tone = tone_types[choice - 1]
                print(f"You selected the tone to be : {selected_tone.value}")
                return selected_tone
            else:
                print(f"Please enter a number between 1 and {len(tone_types)}")
        except ValueError:
            print("Invalid input. Please enter a number.")
