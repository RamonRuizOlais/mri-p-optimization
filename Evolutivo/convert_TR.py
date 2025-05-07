# -*- coding: utf-8 -*-

def convert_to_TR(x, vect_TR):
  return [tr for tr, bins in zip(vect_TR, x) if bins == 1]
