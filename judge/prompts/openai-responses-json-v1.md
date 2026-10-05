OPENAI RESPONSES OUTPUT CONTRACT v1

Return exactly one JSON object matching the supplied strict text.format schema.
Do not emit Markdown fences, duplicate keys, NaN, Infinity, tool calls, or extra
properties. The local adapter supplies request metadata, derived fields, and
stage-inapplicable null/empty fields. Omit the optional legacy data_log2 cost
metadata. JSON validity does not imply proof validity.

Reconstruct the actual claim from the evidence and evaluate it against the rubric.
When citing a target-profile or attack-class identifier, copy it exactly from the
relevant evidence. If the proof and manifest disagree, report that disagreement;
do not silently repair either one.
