def generate_srt(transcript: str, output_path: str) -> str:
    # Basic dummy timestamping: one line per 5 seconds
    lines = transcript.split('.')
    srt_lines = []
    for i, line in enumerate(lines):
        start = i * 5
        end = start + 5
        srt_lines.append(f"{i+1}")
        srt_lines.append(f"00:00:{start:02d},000 --> 00:00:{end:02d},000")
        srt_lines.append(line.strip() + '\n')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(srt_lines))
    return output_path
