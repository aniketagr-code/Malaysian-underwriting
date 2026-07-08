import sys
sys.path.append('C:/Users/lenovo/Downloads/Malaysian underwriting')
from backend.scripts.generate_tests import samples, get_variance
import re

test_cases_str = 'test_cases = [\n'
for idx, row in samples.iterrows():
    req, engine, actual, var = get_variance(row)
    req_dict = req.model_dump()
    for k, v in req_dict.items():
        if hasattr(v, 'value'):
            req_dict[k] = v.value
    test_cases_str += f'    # {row["Risk_Category"]} Risk, Policy: {row["Policy_ID"]}\n'
    test_cases_str += f'    ({req_dict}, {actual}, {actual * 0.15}),\n'
test_cases_str += ']\n'

with open('backend/tests/test_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(r'test_cases = \[.*?\]\n', test_cases_str, content, flags=re.DOTALL)

with open('backend/tests/test_engine.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
