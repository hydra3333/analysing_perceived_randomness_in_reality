"""Add E_2, E_17, E_18 and E_19 to the contract runner's ADAPTERS (four imports, four entries). Usage: TREE"""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'src' / 'methods' / 'Method_Contract_Runner.py'
t = p.read_text()
E = [("from contract_adapters import e_001\n", "from contract_adapters import e_001\nfrom E_002 import contract as e_002\n"),
     ("from E_010 import contract as e_010\n", "from E_010 import contract as e_010\nfrom E_017 import contract as e_017\nfrom E_018 import contract as e_018\nfrom E_019 import contract as e_019\n"),
     ("ADAPTERS = {'E_1': e_001, 'E_3': e_003, 'E_4': e_004, 'E_6': e_006, 'E_7': e_007, 'E_8': e_008, 'E_9': e_009,\n            'E_10': e_010}",
      "ADAPTERS = {'E_1': e_001, 'E_2': e_002, 'E_3': e_003, 'E_4': e_004, 'E_6': e_006, 'E_7': e_007, 'E_8': e_008,\n            'E_9': e_009, 'E_10': e_010, 'E_17': e_017, 'E_18': e_018, 'E_19': e_019}")]
for o, n in E:
    assert t.count(o) == 1, o[:40]
    t = t.replace(o, n)
p.write_text(t)
print('runner edited')
