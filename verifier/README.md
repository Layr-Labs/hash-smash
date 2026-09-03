# HashSmash deterministic verifier

This package is the credential-free, standard-library-only verification layer for the
fixed `sha1-fips180-4-v1` / `ordinary-collision` / 80-round Yukon pilot.

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
