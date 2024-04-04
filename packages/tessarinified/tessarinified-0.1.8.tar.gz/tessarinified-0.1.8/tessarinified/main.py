import math, cmath
import numpy as _np
from collections.abc import Iterable
_SUP = str.maketrans('0123456789', '\u2070\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079')
_SUB = str.maketrans('0123456789', '\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089')
_sign = lambda x: math.copysign(1, x)
def e(n):
 out = [0] * n
 out.append(1)
 return Tsr(out)
def _signsym(x):
 match _sign(x):
  case 1 | 0:
   return '+'
  case -1:
   return '-'
  
 raise ValueError('sign cannot be determined')
def _unpack(a):
 arr = []
 for x in a:
  match x:
   case complex():
    arr += [x.real, x.imag]
   case int() | float():
    arr.append(float(x))
   case Iterable():
    arr += _unpack(x)
   
  
 return arr
def _init(arr):
 arr = _np.trim_zeros(arr, 'b')
 return [] if len(arr) == 0 else [(float(arr[n]) if n < len(arr) else 0)for n in range(2 ** math.ceil(math.log2(len(arr))))]
class Tsr:
 def __init__(self, *args):
  self.v = _init(_unpack(args))
 def dim(self):
  return len(self.v)
 def order(self):
  return int(math.log2(self.dim()))
 def __str__(self, show_zeroes=False):
  return_str = ''
  if self.dim() > 0:
   if not all([x == 0 for x in self.v]):
    for n, v in enumerate(self.v):
     if v != 0 or show_zeroes:
      return_str += f'{_signsym(self.v[n])}{abs(self.v[n])}e{str(n).translate(_SUB)}'
     
    if return_str[0] == '+':
     return_str = return_str[1:]
    
   
  if return_str == '':
   return_str += '0'
  return f'({return_str})'
 def __add(self, other, t):
  if isinstance(other, Tsr):
   arr = []
   for n in range(max(self.dim(), other.dim())):
    s = self.v[n] if n < self.dim() else 0
    o = other.v[n] if n < other.dim() else 0
    arr.append(s + o)
   return Tsr(arr)
  raise TypeError(f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __add__(self, other):
  return self.__add(other, '+')
 def __iadd__(self, other):
  self.v = (self.__add(other, '+=')).v
  return self
 def __sub__(self, other):
  return self.__add(-other, '-')
 def __isub__(self, other):
  self.v = (self.__add(-other, '-')).v
  return self
 def __mul(self, other, t):
  match other:
   case int() | float():
    return Tsr([other * x for x in self.v])
   case Tsr():
    if self.dim() <= 2 and other.dim() <= 2:
     return Tsr(self.native() * other.native())
    else:
     tsr = Tsr()
     for n, s in enumerate(self.v):
      for m, o in enumerate(other.v):
       w = n ^ m
       tsr += e(w) * {1: -s, 0: s}[(n & m) & 1] * o
      
     return tsr
    
   
  raise TypeError(f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __mul__(self, other):
  return self.__mul(other, '*')
 def __rmul__(self, other):
  return self * other
 def __imul__(self, other):
  self.v = (self.__mul(other, '*=')).v
  return self
 def __neg__(self):
  return Tsr([-a for a in self.v])
 def exp(self):
  if self.dim() <= 2:
   return Tsr(math.e ** (self.native()))
  else:
   out = Tsr(1)
   for n, v in enumerate(self.v):
    if n & 1 == 1:
     out *= (math.cosh(v) * Tsr(1) + math.sinh(v) * e(n))
    else:
     out *= (math.cos(v) * Tsr(1) + math.sin(v) * e(n))
    
   return out
  
 def cosh(self):
  return (self.exp() + (-self).exp()) / 2
 def ln(self):
  if self.dim() > 2:
   a = Tsr(self.v[0:self.dim()//2])
   b = Tsr(self.v[self.dim()//2:self.dim()])
   p = -((a - b) / (a.sq() - b.sq()).sqrt()).ln()
   out = (a / p.cosh()).ln() + p * e(self.dim()//2)
   return out
  elif self.dim() == 2:
   return Tsr(cmath.log(self.native()))
  return Tsr(math.log(self.native()))
 def __round__(self, n=1):
  return Tsr([round(x, n) for x in self.v])
 def invert(self):
  if self.dim() <= 2:
   return Tsr(1 / self.native())
  return (-self.ln()).exp()
 def sqrt(self):
  if self.dim() <= 2:
   return Tsr(self.native() ** 0.5)
   
  return (self.ln() / 2).exp()
  
 def sq(self):
  return self * self
 def __truediv(self, other, t):
  match other:
   case int() | float():
    return Tsr([x / other for x in self.v])
   case Tsr():
    return self * other.invert()
   
  raise TypeError(f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __truediv__(self, other):
  return self.__truediv(other, '/')
  
 def __rtruediv__(self, other):
  if isinstance(other, int | float | Tsr):
   return other * self.invert()
  raise TypeError(f'unsupported operand type(s) for /: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __itruediv__(self, other):
  self.v = (self.__truediv(other, '/=')).v
  return self
 def __pow(self, other, t):
  match other:
   case Tsr():
    if self.dim() <= 2 and other.dim() <= 2:
     return Tsr(self.native() ** other.native())
    elif other == Tsr(2):
     return self.sq()
    return (other * self.ln()).exp()
   case int() | float():
    if other == 2:
     return self.sq
    elif self.dim() <= 2:
     return Tsr(self.native() ** other)
    return (other * self.ln()).exp()
   
  raise TypeError(f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __pow__(self, other):
  return self.__pow(other, '**')
 def __rpow__(self, other):
  match other:
   case Tsr():
    if self.dim() <= 2 and other.dim() <= 2:
     return Tsr(other.native() ** self.native())
    else:
     return (other * self.ln()).exp()
    
   case int()| float():
    if self.dim() <= 2:
     return Tsr(other ** self.native())
    else:
     return (other * self.ln()).exp()
    
   
  raise TypeError(f'unsupported operand type(s) for **: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')
 def __ipow__(self, other):
  self.v = (self.__pow(other, '**=')).v
  return self
 def native(self):
  match self.dim():
   case 2:
    return self.v[0] + self.v[1] * 1j
   case 1:
    return self.v[0]
   case 0:
    return 0
   
  raise ValueError(f'unsupported dimension: 2{str(self.order()).translate(_SUP)}')
 

