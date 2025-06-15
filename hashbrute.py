import itertools
import string

def generate_bcrypt_variations(original_hash):
    """Generate all variations of the hash with _ replaced by all bcrypt characters"""
    # Bcrypt's base64 alphabet (., /, A-Z, a-z, 0-9)
    bcrypt_chars = './'

    # Find all positions of underscore
    underscore_positions = [i for i, char in enumerate(original_hash) if char == '_']

    # Generate all possible combinations of replacements
    replacements = itertools.product(bcrypt_chars, repeat=len(underscore_positions))

    # Create all variations
    variations = []
    for replacement_chars in replacements:
        hash_list = list(original_hash)
        for pos, char in zip(underscore_positions, replacement_chars):
            hash_list[pos] = char
        variations.append(''.join(hash_list))

    return variations

# Example usage
original_hash = "$2y$12$ffpj91_xisclmjgknjjn8_zeie9ivv13_f_qcza4digxjlh2zzzm2"
variations = generate_bcrypt_variations(original_hash)

# Save to file
with open("bcrypt_variations.txt", "w") as f:
    f.write("\n".join(variations))

print(f"Generated {len(variations)} variations")
print(f"First 3 examples:")
for i, var in enumerate(variations[:3]):
    print(f"{i+1}. {var}")
print(f"\nSaved all variations to bcrypt_variations.txt")
