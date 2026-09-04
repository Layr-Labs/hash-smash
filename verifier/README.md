# HashSmash deterministic verifier

This package is the credential-free, standard-library-only verification layer for the
legacy `sha1-fips180-4-v1` / `ordinary-collision` / 80-round Yukon pilot, plus the nine
explicitly selected local tracks in [LOCAL_TRACKS.md](../LOCAL_TRACKS.md).

Add `--track md5-s8` (or another registered ID) to each CLI gate for local v2 inputs.
That selection—not participant text—binds the target, round count, digest width, units
and nominal reference. `hash-collision-witness-v2` supports the selected complete-message
hash through the organizer-owned reference implementation. No candidate code executes.
Local scores additionally require `submission_state: ready` and a matching reviewed
package/configuration fingerprint. Draft and nominal-reference values never emit scores.

Run its three workflow gates from the repository root:

```sh
python3 -m verifier intake --candidate candidate --output-dir artifacts/intake
python3 -m verifier certificates --candidate candidate --output artifacts/certificates.json
python3 -m verifier score --candidate candidate --aggregate artifacts/judge-aggregate.json --output score.json
```

The candidate contains `claim.json`, `proof.md`, and optionally
`certificates/manifest.json` plus its declared data files. Objects are closed: unknown
claim and certificate-manifest fields are errors. The intake gate rejects symlinks,
special files, nested certificate directories, undeclared files, executable files,
oversized files, non-UTF-8 proofs, and non-LF proofs. It emits a line-numbered review copy
without modifying the submitted proof.

The only v1 certificate type is `sha1-collision-witness-v1`. It proves only that two
different byte strings have the declared SHA-1 digest; it does not verify an attack's
method or complexity.

The score gate requires the judge aggregate's exact top-level status to be
`ai_qualified`. It ignores any model-provided score and deterministically computes
`time_log2 + memory_log2_bytes` from the validated claim. Other aggregate statuses exit
nonzero and create no score file.

Run the tests with:

```sh
python3 -m unittest discover -v verifier/tests
```
