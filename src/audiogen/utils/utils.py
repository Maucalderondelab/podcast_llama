# src/audiogen/utils/utils.py

import torch
import torchaudio

from audiogen.models import Audio

from pathlib import Path

import re

import nltk
# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt_tab')


__all__ = [
    "load_txt",
    "torch_concat",
    "split_text_balanced",
    "split_long_sentence",
    "analyze_chunks",
]

# >>> load_txt - from Path >>>
def load_txt(fpath: Path | str) -> str:
    fpath = Path(fpath) # works for both str and Path

    # txtPath = Path(dirPath) / fname
    if not fpath.is_file():
        raise FileNotFoundError(f"File '{fpath}' doesn't exist or is not in this location.")
    return fpath.read_text()
# <<< load_txt - from Path <<<


# >>> relative_save - save file to dir w/o full Path >>>
def _realtive_save(audio_segment, sample_rate, **kwargs):
    kval = kwargs.items()
    if "full_path" in kval:
        output_path = kwargs["full_path"]

    torch.save(Path(output_path), audio_segment, sample_rate)
# <<< relative_save - save file to dir w/o full Path <<<


# >>> Concat Torch segments >>>
def torch_concat(
    audio_segments: list[Audio],
    output_path: Path | str | None = None,
) -> Audio:

    group_audio_segments_list = []
    for asg in audio_segments:
        group_audio_segments_list.append(asg)
    
    group_audio_segments_tuple = tuple(group_audio_segments_list)
    group_audio_segments = torch.cat(group_audio_segments_tuple, dim=1)

    sample_rate = audio_segments[0].srate

    if output_path is not None:
        torchaudio.save(Path(output_path), group_audio_segments, sample_rate)
        _print_output = f"DONE! Saved torch-concatenated audio file at: {output_path}"
        print(len(_print_output) * "-")
        print(_print_output)

    return Audio(group_audio_segments, sample_rate) 
# <<< Concat Torch segments <<<


# >>> Split text balanced >>>
def split_text_balanced(text: str, max_length: int = 300, target_length: int | None = None) -> list[str]:
    """
    Split text into sentences with similar lengths, respecting sentence boundaries.
    
    Args:
        text: Input text to split
        max_length: Maximum characters per chunk (default: 256)
        target_length: Target length for each chunk (default: max_length * 0.75)
        
    Returns:
        List of text chunks with similar lengths
    """
    if target_length is None:
        target_length = int(max_length * 1.00)  
    
    # First, split into sentences using NLTK
    sentences = nltk.sent_tokenize(text)
    
    # Clean up sentences (remove extra whitespace)
    sentences = [sent.strip() for sent in sentences if sent.strip()]
    
    chunks = []
    current_chunk = ""
    
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        
        # If single sentence is too long, split it further
        if len(sentence) > max_length:
            # Split long sentence at natural break points
            sub_chunks = split_long_sentence(sentence, max_length, target_length)
            chunks.extend(sub_chunks)
            i += 1
            continue
        
        # Check if adding this sentence would exceed max_length
        potential_chunk = current_chunk + (" " if current_chunk else "") + sentence
        
        if len(potential_chunk) <= max_length:
            current_chunk = potential_chunk
            
            # If we're close to target length, try to balance with next sentences
            if len(current_chunk) >= target_length:
                # Look ahead to see if we should include more sentences for better balance
                lookahead_chunk = current_chunk
                j = i + 1
                
                while j < len(sentences):
                    next_sentence = sentences[j]
                    test_chunk = lookahead_chunk + " " + next_sentence
                    
                    if len(test_chunk) > max_length:
                        break
                    
                    # Calculate how close we'd be to target vs current distance
                    current_distance = abs(len(current_chunk) - target_length)
                    new_distance = abs(len(test_chunk) - target_length)
                    
                    if new_distance < current_distance:
                        lookahead_chunk = test_chunk
                        j += 1
                    else:
                        break
                
                current_chunk = lookahead_chunk
                i = j
                chunks.append(current_chunk)
                current_chunk = ""
                continue
        else:
            # Current sentence doesn't fit, save current chunk and start new one
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
        
        i += 1
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
# <<< Split text balanced <<<


# >>> Split in sentences >>>
def split_long_sentence(sentence: str, max_length: int, target_length: int) -> list[str]:
    """
    Split a sentence that's too long at natural break points.
    
    Args:
        sentence: Long sentence to split
        max_length: Maximum length per chunk
        target_length: Target length per chunk
        
    Returns:
        List of sentence chunks
    """
    # Try to split at natural break points: commas, semicolons, conjunctions
    break_patterns = [
        r'([,;:])\s+',  # Commas, semicolons, colons
        r'\s+(and|but|or|however|therefore|moreover|furthermore|nevertheless)\s+',  # Conjunctions
        r'(\.|!|\?)\s+',  # End of sentences (shouldn't happen much here)
        r'\s+(-|–|—)\s+',  # Dashes
    ]
    
    chunks = []
    remaining = sentence
    
    while len(remaining) > max_length:
        best_split = None
        best_position = 0
        
        # Try each break pattern
        for pattern in break_patterns:
            matches = list(re.finditer(pattern, remaining))
            
            for match in matches:
                split_pos = match.end()
                
                # Check if this split position gives us a good chunk size
                if target_length * 0.5 <= split_pos <= max_length:
                    # Prefer splits closer to target length
                    distance_to_target = abs(split_pos - target_length)
                    if best_split is None or distance_to_target < best_split:
                        best_split = distance_to_target
                        best_position = split_pos
        
        if best_position > 0:
            # Split at the best position found
            chunk = remaining[:best_position].strip()
            chunks.append(chunk)
            remaining = remaining[best_position:].strip()
        else:
            # No good break point found, split at word boundary near target
            words = remaining.split()
            chunk_words = []
            chunk_length = 0
            
            for word in words:
                if chunk_length + len(word) + 1 > max_length:
                    break
                chunk_words.append(word)
                chunk_length += len(word) + 1
            
            if chunk_words:
                chunk = " ".join(chunk_words)
                chunks.append(chunk)
                remaining = remaining[len(chunk):].strip()
            else:
                # Emergency case: split mid-word if necessary
                chunks.append(remaining[:max_length])
                remaining = remaining[max_length:]
    
    # Add remaining text
    if remaining:
        chunks.append(remaining)
    
    return chunks
# <<< Split in sentences <<<


# >>> Analyze text chunks >>>
def analyze_chunks(chunks: list[str]) -> None:
    """
    Print analysis of chunk lengths for debugging.
    
    Args:
        chunks: List of text chunks to analyze
    """
    lengths = [len(chunk) for chunk in chunks]
    
    print(f"Number of chunks: {len(chunks)}")
    print(f"Length statistics:")
    print(f"  Min: {min(lengths)}")
    print(f"  Max: {max(lengths)}")
    print(f"  Average: {sum(lengths) / len(lengths):.1f}")
    print(f"  Standard deviation: {(sum((x - sum(lengths)/len(lengths))**2 for x in lengths) / len(lengths))**0.5:.1f}")
    
    print(f"\nChunk lengths: {lengths}")
    
    for i, chunk in enumerate(chunks):
        # print(f"\nChunk {i+1} ({len(chunk)} chars): {chunk[:100]}{'...' if len(chunk) > 100 else ''}")
        print(f"\nChunk {i+1} ({len(chunk)} chars): {chunk}")
# <<< Analyze text chunks <<<
