"""Simplification functions for SymPy"""

import sympy as sp
from IPython.display import display, Math, Latex, display_latex

def apply_to_numden(expr, fun, numer=True, denom=True):
	"""Apply a function to the numerator, denominator, 
	or both of a SymPy expression
	"""
	num, den = sp.fraction(expr.cancel())
	if numer:
		num = fun(num)
	if denom:
		den = fun(den)
	return num/den

def display_dict(d):
	"""Display a dictionary with pretty-printing"""
	for k, v in d.items():
		display(sp.Eq(k, v))
