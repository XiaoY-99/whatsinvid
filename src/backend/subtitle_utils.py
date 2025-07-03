import os

def generate_srt_and_txt(transcript: str, base_path: str) -> dict:
    """
    Generate both SRT and TXT files from the transcript.
    
    Args:
        transcript (str): The full transcript text.
        base_path (str): The full path **without extension** (e.g., "/path/to/file").
    
    Returns:
        dict: A dictionary with paths to the generated .srt and .txt files.
    """
    # Basic dummy timestamping: one sentence per 5 seconds
    lines = transcript.split('.')
    srt_lines = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        start = i * 5
        end = start + 5
        srt_lines.append(f"{i+1}")
        srt_lines.append(f"00:00:{start:02d},000 --> 00:00:{end:02d},000")
        srt_lines.append(line.strip() + '\n')

    # Output file paths
    srt_path = f"{base_path}.srt"
    txt_path = f"{base_path}.txt"

    # Write .srt
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(srt_lines))

    # Write .txt
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript.strip())

    return {
        "srt": srt_path,
        "txt": txt_path
    }
