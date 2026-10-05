# Terms of Service

HashSmash  · Eigen Labs, Inc.

EFFECTIVE: October 5, 2026

These Terms of Service ("Terms") are a legal agreement between you and Eigen Labs, Inc. ("Eigen Labs," "we," "us," or "our") governing your access to and use of HashSmash, including the HashSmash website,, the Yukon CLI, and related APIs (collectively, the "Platform").

Standalone agreement. These Terms govern HashSmash only. They are separate from and do not incorporate the Eigen Labs Terms of Service governing any other Eigen Labs products, including the terms governing any other Yukon challenge.

By creating an account, installing the CLI, or otherwise using the Platform, you agree to these Terms and our Privacy Policy, which is incorporated by reference. If you are using the Platform on behalf of an organization, you represent that you have authority to bind that organization. If you do not agree, do not use the Platform.

## 1. Eligibility

You may use the Platform only if you are at least 13 years old (16 if you are in the EEA or UK); you have a valid GitHub account; you have access to a computer that can run the Yukon CLI, Git, and Python 3; and your use of the Platform complies with applicable law and does not violate any export control or sanctions restriction.

Age verification: By using the Platform you represent that you meet the applicable minimum age, and you may be asked to confirm your date of birth or age. We do not knowingly permit anyone below the applicable age to use the Platform, and we will terminate accounts and delete associated data on discovery.

## 2. The Platform

HashSmash is a benchmark for AI-assisted review of cryptanalytic collision claims against reduced-round hash functions. Each track specifies a target hash function and round count, a review lane, a common cost model, and a scoring formula. You submit a candidate package (a structured claim, a written argument, and any declared certificates or experiments) via the CLI. Your package is validated, any declared experiments are run in an isolated environment, and the package is then reviewed by AI models. If your package qualifies, your score and a link to the evaluation appear on the leaderboard. Your score is the base-2 logarithm of the total computation your package claims and justifies under the track's cost model; lower is better.

Modifiable surface. You may only modify files within the modifiable surface defined in the challenge documentation (for HashSmash, the editable candidate directory for your assigned track). The harness, target profiles, cost models, schemas, AI review prompts and configuration, verifier, workflows, scoring code, generated scores, other participants’ candidates, and any code subject to any restricted Eigen Labs or third party license are frozen and must not be modified or incorporated into your submission.

Review gate. Qualification is mandatory. Your package must pass intake validation, any declared experiments, and the AI review policy for your selected track. A package that fails validation or does not qualify produces no score. Review outcomes are automated assessments by AI models. They are not mathematical proof, peer review, or human acceptance of your claim, and they do not establish that any attack is practical or that any hash function is insecure.

Winning and promotion. If your submission qualifies and improves on the current best score for its track, it enters manual review. The benchmark owner inspects the recorded candidate commit and may accept or decline it for promotion in its discretion. If accepted, your candidate commit is promoted to the repository's main branch, becoming the new baseline. See Section 5 for what this means for intellectual property.

AI agent submissions. You may use AI coding agents to generate or automate your submission. AI-assisted submissions are permitted. You are responsible for the content of every submission made under your account, regardless of how it was generated. When you use an AI coding agent, the agent’s reasoning traces, chat transcripts, prompts, model outputs, and associated benchmark artifacts may be collected as Covered Data and published as described in Section 5 unless you opt out.

## 3. Accounts and API Keys

Accounts are created by signing in with GitHub OAuth. You are responsible for all activity under your account. Keep your API keys confidential. Do not share them or commit them to source control. You may provide your API keys, including by using a setup prompt the Platform generates for that purpose, to an AI agent you control for the purpose of submitting on your behalf, provided you remain responsible for all activity conducted under your account regardless of how it was generated. A Yukon API key does not provide access to any AI review provider. Never include provider credentials (such as OpenRouter or AWS keys), .env files, or other secrets in any submission, submission note, or research discussion.  If you believe your account or API keys have been compromised, revoke them immediately and notify us at [notices@eigenlabs.org](mailto:notices@eigenlabs.org)

CLI installation. The CLI is installed by running curl -fsSL [https://api.yukon.org/yukon/install.sh](https://api.yukon.org/yukon/install.sh) | sh. By running this command, you execute a shell script from Eigen Labs' servers. You should review the script before running it. Installing the CLI also adds the /yukon-cli skill for use with compatible coding agents.

## 4. Prohibited Conduct

You may not:

- Modify, tamper with, reverse-engineer, or circumvent the frozen harness, scoring code, verifier, AI review pipeline, or any other frozen component.
- Manipulate benchmark measurements, evaluation infrastructure, hardware counters, or any part of the scoring pipeline.
- Attempt to influence the AI review through anything other than the substance of your claim, including by embedding instructions, prompt injections, or other content directed at the reviewing models.
- Submit experiments or other code that attempts to access the network, escape or probe the isolated execution environment, or obtain credentials.
- Edit, fabricate, or reuse generated score files, or misrepresent the resources your claim requires.
- Push changes directly to the benchmark branch, or open, merge, or replace a Yukon submission pull request yourself.
- Incorporate into any submission any Eigen Labs component outside the designated modifiable surface.
- Submit code containing malware, backdoors, exploits, or any code designed to compromise any system.
- Submit code that infringes a third party's intellectual property rights, or that includes third-party code under a license incompatible with the Apache License 2.0.
- Create multiple accounts to circumvent rate limits, disqualifications, or other Platform controls.
- Interfere with or disrupt the integrity or performance of the Platform.
- Use the Platform for any unlawful purpose or in violation of applicable law.

Violations may result in disqualification, account suspension or termination, and removal from the leaderboard, at our discretion.

## 5. Intellectual Property

**Platform access license**. Subject to your compliance with these Terms, Eigen Labs grants you a limited, non-exclusive, non-transferable, revocable license to access and use the Platform solely to participate in challenges as contemplated by these Terms. This license terminates automatically if your access is suspended or terminated under these Terms.

**Platform ownership**. Eigen Labs and its licensors own all rights in the Platform, including the harness, verification and scoring infrastructure, leaderboard, and challenge design. Nothing in these Terms transfers any Eigen Labs intellectual property to you.

**Your submissions**. You retain ownership of your submissions to the extent ownership vests in you. By submitting, you grant Eigen Labs a worldwide, royalty-free, non-exclusive, perpetual license to use, reproduce, display, and distribute your submission to operate the Platform, including displaying it in the public evaluation record and leaderboard.

**Covered Data, Publication and Data License**. In the course of participating in a challenge, particularly if you use an AI coding agent, you may generate reasoning traces, chat transcripts, prompts, model outputs, tool calls and results and associated benchmark artifacts ("Covered Data"). Unless you opt out, Eigen Labs collects Covered Data and may publish a pseudonymized, filtered version of your Covered Data as part of a public dataset of all collected Covered Data from all users. By participating without opting out from the collection of Covered Data, you grant Eigen Labs a worldwide, royalty-free, non-exclusive, perpetual, sublicensable, transferrable license to use, reproduce, modify, create derivative works of and from, analyze, and use to develop, train, fine-tune and evaluate machine-learning models and datasets, and publish or distribute your Covered Data, and to grant further rights in your Covered Data to third parties. Any public release of Covered Data as part of a public dataset will be under the terms of a data license that Eigen Labs will make publicly available at or before the time it first publishes any Covered Data. Eigen Labs will not publish your Covered Data until it has published that license at a publicly accessible URL, but otherwise may use Covered Data as permitted by the above license grant. Covered Data does not include your submission, which is governed exclusively by the grants set forth above and below in this Section 5.

You may opt out of Covered Data collection and publication at any time and doing so will not affect your ability or eligibility to participate in any challenge, your score or your leaderboard placement. You may elect not to have your Covered Data collected by opting-out from within the Yukon CLI. You may also request that already-collected Covered Data be removed from any published dataset by contacting [notices@eigenlabs.org](mailto:notices@eigenlabs.org). We will remove your Covered Data from our own published dataset and any subsequent release we control, and delete it, including any pre-filtering or internal copies, from our internal systems, subject to reasonable operational exceptions no later than our next scheduled release. We will also use reasonable efforts to notify known downstream licensees of your removal request. However, because Covered Data may already have been downloaded, copied, or used to train models or build tools by third parties before your request, we cannot remove it from copies outside our control, and removal does not affect any model or tool already built using that data.

**Pseudonymization and filtering are best-effort, not guaranteed**. Before any publication of Covered Data, Eigen Labs runs an automated pipeline that removes payloads, replaces identifiers with pseudonymous tokens, scrubs credentials and personal data, and applies a privacy filter. No automated filter is perfect. You acknowledge that pseudonymization is not anonymization, that filtering may miss sensitive content, and that once published, data may be copied, cached, mirrored, and indexed by third parties and cannot be fully retracted. You should not enter anything you would not want published into your agent session or prompts, or in any submissions.

**Winning submissions — Apache 2.0 grant**. If your submission is promoted to the repository's main branch, it is incorporated under the Apache License 2.0. By submitting, you grant Eigen Labs and all downstream recipients a perpetual, irrevocable, worldwide, royalty-free license under Apache 2.0 to reproduce, prepare derivative works, publicly display, publicly perform, sublicense, and distribute your submission. Consistent with Apache 2.0, you also grant each recipient a patent license under your essential patent claims necessarily infringed by your submission, and you agree that if you initiate patent litigation alleging your submission constitutes infringement, your patent license to that recipient terminates.  Where your submission incorporates or modifies pre-existing third-party open-source code, that underlying code remains subject to its own license terms notwithstanding the grant above, and Eigen Labs will preserve any required attribution when promoting and redistributing a winning submission.

**Git commit authorship.** When your submission is promoted, the merge commit will include a Co-authored-by: trailer with your GitHub username and a GitHub-generated noreply email address, as described in the Privacy Policy. This is a permanent, public part of the repository's git history. By submitting, you explicitly consent to this disclosure.

**Representations.** By submitting, you represent that you have all rights needed for the license grants above; your submission does not infringe any third-party intellectual property rights; it contains no code under a license incompatible with Apache 2.0; and if AI-assisted, you have reviewed it and take full responsibility for its content. You further represent that your Covered Data does not contain any third party’s personal information, confidential information, trade secrets or credentials that you lack the right to disclose, and does not contain your own or any third party’s sensitive personal data that you do not, or such third party would not, wish collected or published.

## 6. Leaderboard and Public Information

The leaderboard is public. By submitting, you consent to public display of your GitHub username, avatar, profile link, account UUID, submission note, scores and metrics, status, timestamps, commit SHAs, and a link to the public evaluation record containing your code.

Your submitted proofs, code, notes, verification artifacts, evaluation records, AI review dossiers and findings, experiment outputs, research discussion posts, and promotion commits may be public. Do not include sensitive personal data, credentials, secrets, confidential information, trade secrets, or anything else you do not have the right to disclose or do not want publicly disclosed in any submission or related material.

Submission data and promotion commits form part of the immutable competition record. You may not request removal of leaderboard data or git history on the basis that you no longer wish it displayed. Contact us to discuss individual circumstances. This immutable competition record is separate from your Covered Data, which you may decline or have removed from the published dataset as described in Section 5.

## 7. Third-Party Services

The Platform integrates with GitHub (OAuth, repository hosting, research discussions, and the GitHub Actions workflows that validate submissions, run declared experiments, and perform AI review and scoring), Supabase (authentication and database), Cloudflare (submission storage), Vercel and Fly.io (hosting), and Amazon Web Services (Amazon Bedrock) and OpenRouter (access to the third-party AI models that review submissions). Your use of these services is subject to their own terms. By submitting, you consent to your submission, including your claim, proof, certificates, and experiment results, being transmitted to and processed by these services and the AI models that review it, as necessary to operate the Platform. Eigen Labs is not responsible for the availability, accuracy, or practices of any third-party service. The Platform may also use a third-party service, such as Hugging Face, to host any public dataset of pseudonymized, filtered Covered Data. Unless you opt out from the publication of your Covered Data, you consent to your Covered Data being transmitted to and processed by such services to operate the Platform and publish the dataset.

## 8. Disclaimers

THE PLATFORM IS PROVIDED "AS IS" AND "AS AVAILABLE." TO THE MAXIMUM EXTENT PERMITTED BY LAW, EIGEN LABS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT.

Eigen Labs does not warrant that the Platform will be uninterrupted or error-free; that benchmark scores are free from measurement error; that any submission will be evaluated, accepted, or promoted; or that winning submissions are free from defects. Eigen Labs does not warrant that pseudonymization or filtering of Covered Data is complete or error-free.

Eigen Labs does not warrant that any AI review outcome, finding, or score is correct, complete, or consistent across submissions. Review outcomes are generated by third-party AI models, are not mathematical proof or human acceptance of any claim, and may change if submissions are rescored under updated review rules.

The Platform is a research benchmark for technical users.  You assume all risks associated with running third-party code on your hardware.  Run the challenge only in an environment you are willing to expose to untrusted code.

## 9. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, EIGEN LABS AND ITS AFFILIATES, OFFICERS, DIRECTORS, EMPLOYEES, AND CONTRACTORS WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS, DATA, GOODWILL, OR BUSINESS INTERRUPTION, EVEN IF ADVISED OF THE POSSIBILITY OF THOSE DAMAGES.

OUR AGGREGATE LIABILITY FOR ALL CLAIMS ARISING OUT OF OR RELATING TO THE PLATFORM OR THESE TERMS WILL NOT EXCEED THE GREATER OF (A) AMOUNTS YOU HAVE PAID TO EIGEN LABS IN THE TWELVE MONTHS BEFORE THE CLAIM OR (B) USD $100.

These limitations do not apply to liability that cannot be excluded under applicable law.

## 10. Indemnification

You will defend, indemnify, and hold harmless Eigen Labs and its affiliates, officers, directors, employees, and contractors from and against any third-party claims, liabilities, damages, losses, and expenses (including reasonable attorneys' fees) arising from your use of the Platform; your submissions, including any claim that a submission infringes third-party intellectual property; your violation of these Terms; or your violation of applicable law. This includes any third-party claim that your Covered Data contained personal, confidential or proprietary information that you lacked the right to disclose.

## 11. Suspension and Termination

We may suspend or terminate your access immediately, with or without notice, if you breach these Terms or applicable law, your use creates legal or security risk, or we discontinue the Platform. You may stop using the Platform at any time.

Sections 5 (Intellectual Property), 6 (Leaderboard), 8 (Disclaimers), 9 (Limitation of Liability), 10 (Indemnification), 12 (Dispute Resolution), and any other provisions that by their nature should survive, will survive termination. Termination does not affect public git history or leaderboard records already disclosed.

## 12. Dispute Resolution, Arbitration, and Governing Law

PLEASE READ THIS SECTION CAREFULLY. IT MAY SIGNIFICANTLY AFFECT YOUR LEGAL RIGHTS, INCLUDING YOUR RIGHT TO FILE A LAWSUIT IN COURT AND TO HAVE A JURY HEAR YOUR CLAIMS. IT CONTAINS PROCEDURES FOR MANDATORY BINDING ARBITRATION AND A CLASS ACTION WAIVER.

BY AGREEING TO THESE TERMS, YOU AGREE (A) TO RESOLVE ALL DISPUTES (WITH LIMITED EXCEPTION) RELATED TO THE PLATFORM THROUGH BINDING INDIVIDUAL ARBITRATION, WHICH MEANS THAT YOU WAIVE ANY RIGHT TO HAVE THOSE DISPUTES DECIDED BY A JUDGE OR JURY, AND (B) TO WAIVE YOUR RIGHT TO PARTICIPATE IN CLASS ACTIONS, CLASS ARBITRATIONS, OR REPRESENTATIVE ACTIONS, AS SET FORTH BELOW. YOU HAVE THE RIGHT TO OPT-OUT OF THE ARBITRATION CLAUSE AND THE CLASS ACTION WAIVER AS EXPLAINED IN SECTION 12.8.

### 12.1 Informal process first.

Before starting arbitration or court proceedings, the party with a claim must send the other a written notice describing the dispute and requested relief. The parties will try in good faith to resolve it informally for 30 days. Both parties agree that this informal dispute resolution procedure is a condition precedent which must be satisfied before initiating any arbitration.

### 12.2 Agreement to arbitrate.

Except as described in Section 12.4, any dispute, claim, or controversy arising out of or relating to these Terms or the Platform will be resolved by final and binding individual arbitration, including threshold questions of arbitrability of the claim . The arbitration will be administered by JAMS under its then-current Comprehensive Arbitration Rules; conducted in English before a single arbitrator; and governed by the Federal Arbitration Act to the extent applicable. Because these Terms concern interstate commerce, the FAA governs the arbitrability of all disputes. However, the arbitrator will apply applicable substantive law consistent with the FAA and the applicable statute of limitations or condition precedent to suit. Judgment on the arbitration award may be entered in any court that has jurisdiction. Any arbitration under these Terms will take place on an individual basis — class arbitrations and class actions are not permitted. You understand that by agreeing to these Terms, you and Eigen Labs are each waiving the right to trial by jury or to participate in a class action or class arbitration.

### 12.3 Batch arbitration.

To increase the efficiency of administration and resolution of arbitrations, you and Eigen Labs agree that in the event that there are one hundred (100) or more individual claims of a substantially similar nature filed against Eigen Labs by or with the assistance of the same law firm, group of law firms, or organizations within a thirty (30) day period, JAMS shall: (1) administer the arbitration demands in batches of 100 claims per batch (plus, to the extent there are fewer than 100 claims remaining after the initial batching, a final batch consisting of the remaining claims); (2) appoint one arbitrator for each batch; and (3) provide for the resolution of each batch as a single consolidated arbitration with one set of filing and administrative fees due per side per batch, one procedural calendar, one hearing (if any), and one final award ("Batch Arbitration"). All parties agree that claims are of a "substantially similar nature" if they arise out of or relate to the same event or factual scenario and raise the same or similar legal issues and seek the same or similar relief. To the extent the parties disagree on whether the Batch Arbitration process applies, JAMS shall appoint a sole standing arbitrator to determine applicability, whose fees shall be paid by Eigen Labs. This Batch Arbitration provision shall not be interpreted as authorizing a class, collective, or mass arbitration of any kind, except as expressly set forth in this provision.

### 12.4 Exceptions.

The following may be brought in court: qualifying claims in small claims court as long as brought and maintained as an individual dispute and not as a class or representative action; claims where the sole form of relief sought is injunctive relief (including public injunctive relief) claims seeking only injunctive relief; or claims relating to intellectual property disputes.

### 12.5 Arbitration fees.

Fees are governed by the applicable JAMS rules. If the arbitrator determines those costs would be prohibitively more expensive for you than court, Eigen Labs will pay the portion necessary to avoid that result, subject to possible reimbursement as set forth in Section 12.6.

### 12.6 Fees, frivolous claims, and settlement.

Fees and costs may be awarded as provided pursuant to applicable law. If the arbitrator finds that either the substance of your claim or the relief sought is frivolous or brought for an improper purpose (as measured by the standards set forth in Federal Rule of Civil Procedure 11(b)), then the payment of all fees will be governed by the JAMS Rules and you agree to reimburse Eigen Labs for all monies previously disbursed by it that are otherwise your obligation to pay under the applicable rules. If you prevail in the arbitration and are awarded an amount that is less than the last written settlement amount offered by Eigen Labs before the arbitrator was appointed, Eigen Labs will pay you the amount it offered in settlement. The arbitrator may make rulings and resolve disputes as to the payment and reimbursement of fees or expenses at any time during the proceeding and upon request from either party made within fourteen (14) days of the arbitrator's ruling on the merits.

### 12.7 Opt-out.

You may opt out of this arbitration agreement by sending written notice to [notices@eigenlabs.org](mailto:notices@eigenlabs.org) within 30 days after your first use of the Platform or first agreement to these Terms. Your notice must include your name, account information, and a clear statement that you want to opt out. If you opt out, the class-action waiver in Section 12.8 still applies to the maximum extent permitted by law. If you opt-out of these arbitration provisions, Eigen Labs also will not be bound by them.

### 12.8 Class action waiver.

TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW, YOU AND EIGEN LABS EACH AGREE THAT ANY PROCEEDING TO RESOLVE ANY DISPUTE, CLAIM, OR CONTROVERSY WILL BE BROUGHT AND CONDUCTED ONLY IN THE RESPECTIVE PARTY'S INDIVIDUAL CAPACITY AND NOT AS PART OF ANY CLASS (OR PURPORTED CLASS), CONSOLIDATED, MULTIPLE-PLAINTIFF, OR REPRESENTATIVE ACTION OR PROCEEDING ("CLASS ACTION"). YOU AND EIGEN LABS AGREE TO WAIVE THE RIGHT TO PARTICIPATE AS A PLAINTIFF OR CLASS MEMBER IN ANY CLASS ACTION.

EIGEN LABS AND YOU EXPRESSLY WAIVE ANY ABILITY TO MAINTAIN A CLASS ACTION IN ANY FORUM. IF THE DISPUTE IS SUBJECT TO ARBITRATION, THE ARBITRATOR WILL NOT HAVE THE AUTHORITY TO COMBINE OR AGGREGATE CLAIMS, CONDUCT A CLASS ACTION, OR MAKE AN AWARD TO ANY PERSON OR ENTITY NOT A PARTY TO THE ARBITRATION. FURTHER, YOU AND EIGEN LABS AGREE THAT THE ARBITRATOR MAY NOT CONSOLIDATE PROCEEDINGS FOR MORE THAN ONE PERSON'S CLAIMS AND MAY NOT OTHERWISE PRESIDE OVER ANY FORM OF CLASS ACTION. FOR THE AVOIDANCE OF DOUBT, YOU CAN SEEK PUBLIC INJUNCTIVE RELIEF TO THE EXTENT AUTHORIZED BY LAW AND CONSISTENT WITH THE EXCEPTIONS CLAUSE IN SECTION 12.4. IF THIS CLASS ACTION WAIVER IS LIMITED, VOIDED, OR FOUND UNENFORCEABLE, THEN, UNLESS THE PARTIES MUTUALLY AGREE OTHERWISE, THE PARTIES' AGREEMENT TO ARBITRATE SHALL BE NULL AND VOID WITH RESPECT TO SUCH PROCEEDING SO LONG AS THE PROCEEDING IS PERMITTED TO PROCEED AS A CLASS ACTION. IF A COURT DECIDES THAT THE LIMITATIONS OF THIS PARAGRAPH ARE DEEMED INVALID OR UNENFORCEABLE, ANY PUTATIVE CLASS OR REPRESENTATIVE ACTION MUST BE BROUGHT IN A COURT OF PROPER JURISDICTION AND NOT IN ARBITRATION.

### 12.9 Governing law and venue.

These Terms are governed by the laws of the State of New York, without regard to conflict-of-laws principles. For any claim not subject to arbitration, you and Eigen Labs consent to the exclusive jurisdiction of the state and federal courts in New York, New York.

## 13. Changes to These Terms

We may modify these Terms from time to time. When we make material changes, we will update the date above and, where appropriate, notify you by email or platform notice. Continued use after the effective date constitutes acceptance. If you do not agree, stop using the Platform.

## 14. Miscellaneous

Entire agreement. These Terms and the Privacy Policy are the entire agreement between you and Eigen Labs regarding the Platform.

Severability. If any provision is held unenforceable, it will be modified to the minimum extent necessary, and the rest will remain in effect.

Waiver. Our failure to enforce any provision is not a waiver.

Assignment. You may not assign these Terms without our written consent. We may assign them freely, including in connection with a merger, acquisition, or sale of assets.

No third-party beneficiaries. These Terms do not create third-party beneficiary rights.

## 15. Contact

For questions about these Terms:

Eigen Labs, Inc.

600 1st Ave Ste 330 # 926277

Seattle, WA 98104-2246

[notices@eigenlabs.org](mailto:notices@eigenlabs.org)
