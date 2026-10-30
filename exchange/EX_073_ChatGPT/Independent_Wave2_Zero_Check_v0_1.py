import itertools,time
from decimal import Decimal, localcontext
import importlib.util, pathlib
p=pathlib.Path(__file__).with_name("reference_wave2.py")
spec=importlib.util.spec_from_file_location("reference_wave2",p)
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
W=R.ZERO_WITNESS
a=R.log_age_coefficients(W,1,2)
assert a=={1:6,2:-12,3:0,4:6},a
assert R.prime_exponents(a)=={}
assert R.prime_exponents_by_sieve(a)=={}
assert R.direct_sign(a)==R.certified_sign(R.prime_exponents(a))==0
assert R.e17_logage_sign(W,1,2,1)[1]==0
st=time.perf_counter()
try:
    R.certified_sign({k:c for k,c in a.items() if c})
    raise AssertionError('no refusal')
except ValueError as e:
    assert 'cap' in str(e)
print('zero witness + fail-closed cap',round(time.perf_counter()-st,3),'sec')
# Distinct factorization algorithms agree for every coefficient vector in [-2,2]^6
num=0;zero=0;nonzero=0
for cs in itertools.product(range(-2,3),repeat=6):
    d={k:v for k,v in enumerate(cs,1)}
    e=R.prime_exponents(d)
    s=R.prime_exponents_by_sieve(d)
    assert e==s,(cs,e,s)
    if not e:
        assert R.direct_sign(d)==0
        zero+=1
    elif num%97==0:
        sign=R.direct_sign(d)
        with localcontext() as ctx:
            ctx.prec=90
            val=sum((Decimal(c)*Decimal(k).ln() for k,c in d.items()), Decimal(0))
            assert sign==(val>0)-(val<0),(cs,sign,val)
        nonzero+=1
    num+=1
print('exhaustive coefficient arrays:',num,'zero combinations:',zero,'decimal nonzero checks:',nonzero)
# check nonzero source independence: sabotage method route; verifier still works
old=R.prime_exponents
R.prime_exponents=lambda _: (_ for _ in ()).throw(AssertionError('method route called'))
assert R.direct_sign({2:-1,4:1})==1
assert R.direct_sign({2:2,4:-1})==0
R.prime_exponents=old
print('source-route isolation checks PASS')
