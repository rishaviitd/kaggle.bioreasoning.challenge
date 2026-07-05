try:
    import tiktoken
    with open("src/track_one/output/best_instructions.txt", "r", encoding="utf-8") as f:
        text = f.read()
    # Use cl100k_base which is standard for GPT-4/GPT-OSS models
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = len(enc.encode(text))
    words = len(text.split())
    print(f"Exact Token Count (tiktoken): {tokens}")
    print(f"Word Count: {words}")
except ImportError:
    with open("src/track_one/output/best_instructions.txt", "r", encoding="utf-8") as f:
        text = f.read()
    words = len(text.split())
    # Rough estimate (1 token ~= 0.75 words)
    tokens = int(words / 0.75)
    print("tiktoken not installed. Using estimation.")
    print(f"Word Count: {words}")
    print(f"Estimated Token Count: ~{tokens}")
