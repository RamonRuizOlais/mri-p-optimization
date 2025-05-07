# -*- coding: utf-8 -*-

# tf: tiempo/iteracion final (199)
# o: diversidad inicial (D0 | 0.1 | 0.25 | 0.5 | 0.75)
# t: tiempo/iteracion

def Th(t, tf, o):
  return o - (t*(o/tf))
  
