# QSP — Quantum Security Verification

> **From Quantum-Security Claims to Verifiable Evidence.**

QSP is an open verification project exploring how claims about post-quantum and quantum-security systems can be transformed into reproducible, inspectable, and independently verifiable evidence.

The central question is simple:

> **When someone claims that a system is quantum-safe, what can an independent third party actually verify from the available evidence?**

QSP does not treat the use of PQC, QKD, or any single cryptographic technology as proof that an entire system is quantum-safe.

Instead, QSP focuses on the evidence behind the claim.

---

## Start Here

QSP explores a verification chain such as:

**Claim → Evidence → Verification → Reproduction → Independent Re-verification → Assessment**

At every step, the scope of the evidence matters.

A claim should not be trusted beyond what the available evidence can independently demonstrate.

---

## What is Quantum Security Verification?

**Quantum Security Verification (QSV)** is the practice of evaluating quantum-security claims through reproducible evidence, explicit verification boundaries, and independent re-verification.

Rather than asking only:

> “Does this system use post-quantum cryptography?”

QSV asks:

> “What exactly was implemented, what evidence was produced, what was independently verified, and what remains unverified?”

The goal is not to replace cryptographic standards, formal security proofs, certification, or professional security assessment.

The goal is to make the evidence behind quantum-security claims easier to inspect, reproduce, challenge, and independently verify.

---

## What QSP Explores

QSP currently explores areas including:

- Post-Quantum Cryptography (PQC)
- Cryptographic Agility
- PQC Migration Evidence
- Public-Key and Artifact Binding
- Cross-Implementation Verification
- Deterministic Re-verification
- Cross-Platform Reproducibility
- Evidence Portability
- QKD Evidence Classification
- Software Supply Chain Integrity
- External Timestamp Evidence
- Independent Verification
- Independent Assessment Readiness

---

## Verification Model

QSP distinguishes between different evidence states instead of collapsing them into a single “secure / insecure” result.

Examples include:

**Claimed → Evidenced → Verified → Independently Re-verified**

QSP also explicitly records states such as:

**Not Verified · Pending · Unknown · Out of Scope · Fail-Closed**

This distinction is important because the existence of a cryptographic feature does not automatically prove the security of the entire system.

---

## Core Principle

> **Do not trust a quantum-security claim beyond what its evidence can independently demonstrate.**

QSP is designed around explicit evidence boundaries.

Where evidence is incomplete, unavailable, pending, or outside the verification scope, the project should say so rather than silently upgrading the result into a stronger security claim.

---

## Evidence Architecture

The project has progressively explored an evidence chain involving concepts such as:

**Security Claim**

↓

**Reproducible Evidence**

↓

**Cryptographic Binding**

↓

**Execution / Verification Evidence**

↓

**Independent Re-verification**

↓

**Cross-Implementation Verification**

↓

**Evidence Preservation**

↓

**External Timestamp / Public Anchoring**

↓

**Independent Assessment Package**

The exact guarantees depend on the evidence available at each stage.

---

## Key Verification Stages

The following repositories are representative entry points into the QSP verification work.

### Stage380 — Independent Verification Package

Packages an established verification scope into a deterministic, offline, fail-closed verification contract.

Current boundary: package integrity verification is implemented, while formal independent verification remains dependent on upstream acceptance conditions.

https://github.com/mokkunsuzuki-code/stage380

### Stage381 — Cross-Platform Deterministic Re-verification

Extends Stage380 with deterministic comparison across Ubuntu, Windows, and macOS using fixed canonicalization rules and fail-closed comparison logic.

Formal cross-platform completion requires matching results from all required environments.

https://github.com/mokkunsuzuki-code/stage381

### Stage386 — PQC Independent Re-verification & Public-Key Binding

Re-establishes the original Stage375 ML-DSA-65 public-key identity and independently re-verifies the historical PQC signature using publicly available verification material.

Current recorded decision:

`pqc_independent_reverification_verified`

https://github.com/mokkunsuzuki-code/stage386

### Stage387 — PQC Multi-Implementation Interoperability

Extends PQC verification beyond a single implementation by testing multi-implementation interoperability and verifier independence.

This stage is intended to reduce dependence on a single verifier implementation.

https://github.com/mokkunsuzuki-code/stage387

### Stage388 — Independent Assessment Readiness

Packages verification scope, evidence, known limitations, threat assumptions, and reproducibility material for independent technical assessment.

Stage388 represents assessment readiness; it does not claim that an external assessment has already been completed.

https://github.com/mokkunsuzuki-code/stage388

### Stage390 — Independent Third-Party Assessment Intake

Provides the current public entry point for independent third-party replication and assessment-oriented verification work.

Stage390 is an assessment intake and evidence-handling layer. It should not be interpreted as proof that formal external certification or system-wide quantum-safe acceptance has already occurred.

https://github.com/mokkunsuzuki-code/stage390

---

## What QSP Does NOT Claim

This section is intentionally explicit.

QSP does **not** claim that:

- an entire system is quantum-safe merely because PQC is present;
- QKD automatically makes a system secure;
- every historical QSP stage has been independently verified by an external organization;
- QSP constitutes formal certification;
- QSP replaces NIST standards, security audits, formal proofs, or accredited assessment;
- experimental evidence proves properties outside its defined verification scope.

Where external assessment has not occurred, QSP should not represent it as completed.

Where evidence is pending, the state should remain pending.

---

## Reproduce, Verify, Challenge

QSP is intended to be examined rather than simply trusted.

Independent researchers, security engineers, cryptographers, and reviewers are encouraged to:

- inspect the evidence;
- reproduce verification procedures;
- test results in independent environments;
- identify incorrect assumptions;
- challenge verification boundaries;
- report non-reproducible results;
- propose stronger verification methods.

A failed independent reproduction is valuable evidence too.

---

## Project Structure

QSP has been developed incrementally through numbered stages.

The stage repositories preserve the evolution of individual verification mechanisms and experiments.

This repository serves as the **public entry point and navigation layer** for that work.

It does not replace the underlying evidence repositories.

---

## Current Status

QSP is an evolving independent research and open verification project.

Some components demonstrate implemented verification mechanisms.

Other components remain experimental, pending external assessment, or limited to explicitly defined evidence scopes.

The project therefore distinguishes carefully between:

**implemented**

**tested**

**verified**

**independently re-verified**

and

**not yet externally assessed**

---

## Independent Review

Technical criticism is welcome.

If you find:

- a reproducibility failure,
- an incorrect security assumption,
- an evidence-binding problem,
- an interoperability issue,
- an unclear verification boundary,
- or a stronger way to test a claim,

please open an issue in the relevant repository.

The objective is not to make QSP difficult to criticize.

The objective is to make its claims **possible to test**.

---

## Mission

### From Quantum-Security Claims to Verifiable Evidence.

QSP explores how security claims for the post-quantum era can be accompanied by evidence that another person can inspect, reproduce, and independently verify.

---

## Maintainer

**Motohiro Suzuki**

Quantum Security Verification / QSP

GitHub: https://github.com/mokkunsuzuki-code

---

## License

MIT License
