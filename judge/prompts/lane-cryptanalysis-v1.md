Audit the claimed collision construction and the exact probability analysis for
the selected target and round count. Check padding, IV, message length, truncation,
round indexing, output equality, and distinctness of messages. Reject no method
solely for being heuristic. Record score-critical heuristic statements with their
tested and extrapolated scope, dependence assumptions, and sensitivity.

Search for concrete counterexamples and invalid inferences. A candidate fatal
finding must show why the submitted conclusion or bound fails, not merely why it
has not yet been proved. Link findings to collision_correctness,
probability_analysis, or heuristic_justification. A missing material argument is
unresolved and blocks rigorous qualification while preserving exploratory
plausibility if the common evaluability requirements hold.
