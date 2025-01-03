# scripts/preprocess.py
import re
import os

def load_code(file_path):
    """
    Reads the content of the input code file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def remove_comments(code, language='Python'):
    """
    Removes comments from the source code based on the language.
    Supports Python and C-style comments.
    """
    if language == 'Python':
        # Remove single-line Python comments
        code = re.sub(r'#.*', '', code)
    else:
        # Remove C-style comments: single-line // and multi-line /* */
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def normalize_spacing(code):
    """
    Normalizes spacing by removing extra spaces, tabs, and blank lines.
    """
    # Replace tabs with spaces
    code = code.replace('\t', '    ')
    # Remove trailing spaces
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)
    # Remove consecutive blank lines
    code = re.sub(r'\n\n+', '\n', code)
    return code

def hardcoded_optimizations(code):
    """
    Applies hardcoded optimizations to known inefficient patterns in the code.
    """
    # Optimization 1: Replace nested loops with a list comprehension
    if "result = []" in code and "for i in range(" in code and "for j in range(" in code:
        code = code.replace(
            "result = []\nfor i in range(10):\n    for j in range(10):\n        result.append(i * j)",
            "result = [i * j for i in range(10) for j in range(10)]"
        )

    # Optimization 2: Replace string concatenation in a loop with join()
    if "sentence = ''" in code and "for word in words:" in code and "sentence += word + ' '" in code:
        code = code.replace(
            "sentence = ''\nfor word in words:\n    sentence += word + ' '",
            "sentence = ' '.join(words) + ' '"
        )

    # Optimization 3: Replace manual sum calculation with built-in sum()
    if "total = 0" in code and "for num in numbers:" in code and "total += num" in code:
        code = code.replace(
            "total = 0\nfor num in numbers:\n    total += num",
            "total = sum(numbers)"
        )

    # Optimization 4: Replace list-based uniqueness with set-based
    if "unique_items = []" in code and "for item in items:" in code and "if item not in unique_items:" in code:
        code = code.replace(
            "unique_items = []\nfor item in items:\n    if item not in unique_items:\n        unique_items.append(item)",
            "unique_items = list(set(items))"
        )

    return code

def preprocess_code(file_path, language='Python'):
    """
    Main function to preprocess the code.
    Steps:
        1. Load code from file.
        2. Remove comments.
        3. Normalize spacing.
        4. Apply hardcoded optimizations.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load the code
    code = load_code(file_path)
    print("Step 1: Loaded code successfully.")

    # Remove comments
    code_no_comments = remove_comments(code, language)
    print("Step 2: Removed comments.")

    # Normalize spacing
    cleaned_code = normalize_spacing(code_no_comments)
    print("Step 3: Normalized spacing and formatting.")

    # Apply hardcoded optimizations
    optimized_code = hardcoded_optimizations(cleaned_code)
    print("Step 4: Applied hardcoded optimizations.")

    return optimized_code

def save_preprocessed_code(output_path, code):
    """
    Saves the preprocessed code to the specified output file.
    """
    with open(output_path, 'w') as file:
        file.write(code)
    print(f"Preprocessed code saved to: {output_path}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Preprocess source code for analysis and optimization.")
    parser.add_argument('--input', type=str, required=True, help="Path to the input code file.")
    parser.add_argument('--output', type=str, required=True, help="Path to save the preprocessed code.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language of the code (default: Python).")
    args = parser.parse_args()

    # Preprocess the code
    try:
        preprocessed_code = preprocess_code(args.input, args.language)
        save_preprocessed_code(args.output, preprocessed_code)
        print("Code preprocessing completed successfully.")
    except Exception as e:
        print(f"Error: {e}")