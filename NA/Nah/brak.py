import re

def extract_innermost_bracket_text(text):
    # Regex pattern to find the innermost brackets and capture the text within them
    pattern = r'\[(?![^\[\]]*\[)([^\[\]]+)\]'
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    # Return the last match, which will be the innermost brackets' text
    return matches[-1] if matches else None

# Examples
text1 = "This is a [sample [text with [nested] brackets]]"
text2 = "Mismatched [brackets [example"
text3 = "No brackets here"
text4 = "[outer [inner] outer]"

print(extract_innermost_bracket_text(text1))  # Output: "nested"
print(extract_innermost_bracket_text(text2))  # Output: None (no complete innermost pair)
print(extract_innermost_bracket_text(text3))  # Output: None (no brackets)
print(extract_innermost_bracket_text(text4))  # Output: "inner"
