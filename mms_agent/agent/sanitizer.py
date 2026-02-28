def clean_llm_output(raw):
    lines = raw.split("\n")
    clean = []
    for line in lines:
        s = line.strip()
        if s.startswith("```"): continue
        if s.startswith("内容如下"): continue
        if s.startswith("modules/"): continue
        if s.startswith("这是"): continue
        if s in ("...", "",): continue
        clean.append(line)
    return "\n".join(clean).strip() + "\n"
