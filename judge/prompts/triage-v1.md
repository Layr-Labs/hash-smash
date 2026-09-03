Perform triage only. Decide whether the package is ready for specialist review.

Check the target profile and attack class, internal consistency of rounds and costs,
presence of the central reasoning, linkage of declared artifacts, compatibility with
the current frontier, and only obvious fatal errors demonstrated directly by the
evidence. Do not attempt full correctness or complexity review. Do not reject a method
because it is unfamiliar. A repairable ambiguity requires clarification.

Set `decision` to `pass_to_review`, `clarification_needed`, or `out_of_scope`. The
stage-specific response schema omits `verdict`, both cost vectors, and the calculation
trace; do not add them. The trusted runner restores their canonical null/null/empty
values. Reconstruct the submitted claim, identify issues and missing explanations, and
give specific author questions. Use `out_of_scope` only for a demonstrated scope/target
mismatch, represented as a fatal issue.
