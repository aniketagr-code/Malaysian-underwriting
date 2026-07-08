import os

files_to_check = [
    'backend/app/validation.py',
    'backend/scripts/generate_tests.py',
    'backend/scripts/phase1_analysis.py',
    'backend/scripts/phase2_rates.py'
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if r"\'" in content:
            new_content = content.replace(r"\'", "'")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed escaping in {filepath}')
        else:
            print(f'No escaping issues found in {filepath}')
