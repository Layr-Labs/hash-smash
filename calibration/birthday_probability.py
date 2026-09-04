"""Exact arithmetic for a proposed concrete-function birthday argument.

Organizer-owned analysis, not participant code or a complete replacement attack.
Sampling is iid over a finite input domain; repeated inputs are subtracted.
"""
from fractions import Fraction
from math import factorial


def no_output_collision_probability(fiber_sizes: tuple[int, ...], draws: int) -> Fraction:
    """Exact iid probability for a SMALL finite function, via elementary symmetry."""
    if not fiber_sizes or any(type(c) is not int or c < 0 for c in fiber_sizes):
        raise ValueError("fiber sizes must be nonnegative integers")
    domain = sum(fiber_sizes)
    if domain == 0 or type(draws) is not int or not 0 <= draws <= 100:
        raise ValueError("requires nonempty domain and 0 <= draws <= 100")
    if draws > len(fiber_sizes):
        return Fraction(0)
    elementary = [1] + [0]*draws
    for count in fiber_sizes:
        for degree in range(draws, 0, -1):
            elementary[degree] += count*elementary[degree-1]
    return Fraction(factorial(draws)*elementary[draws], domain**draws)


def rational_success_lower_bound(draws: int, outputs: int, domain: int) -> Fraction:
    """Use exp(x) >= 1+x+x^2/2+x^3/6 and subtract repeated-input probability.

Valid for every fixed function between sets of these sizes. This is an analytical
lower bound, not a measured/exact probability. No input domain is materialized.
"""
    if any(type(v) is not int or v < 1 for v in (draws, outputs, domain)):
        raise ValueError("positive integer sizes are required")
    pairs = draws*(draws-1)//2
    x = Fraction(pairs, outputs)
    exp_lower = 1+x+x*x/2+x*x*x/6
    return max(Fraction(0), 1-1/exp_lower-Fraction(pairs, domain))
