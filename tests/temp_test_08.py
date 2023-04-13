from tests import test_prover as tp
from tests import test_rules as tr
import time

now = time.time()

tp.test_09()
# tr.test_rd58()

print(time.time() - now)
