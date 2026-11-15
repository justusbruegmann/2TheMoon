<!--
ARCHITECTURE DECISION RECORD — one file per decision.
- Copy this file to docs/decisions/ADR-[NN]_[short-title].md, e.g., ADR-01_modular-monolith.md,
  and list it in section 2.2 of your SAD.
- Replace every [placeholder] in square brackets. Comments like this one are invisible on GitHub;
  delete them once a part is done.
- Keep it short: one page is plenty. Worked examples: Task 9, and Lecture 9, slides 23 to 25.
- Once accepted, an ADR is not rewritten. If you change your mind, write a new ADR and set this
  one to "superseded by ADR-xx".
-->

# ADR-01 The market simulation needs to run on a dedicated gameserver

| Status   | Date       | Author    |
|----------|------------|-----------|
| accepted | 21.10.2026 | Sebastian |

## Context

<!-- Two to five sentences: what forces this decision? Name scenarios and constraints from
     SAD section 3 by their IDs, and the facts that matter (team size, hosting, load). -->

At the core of the 2TheMoon trading game lies simulation for any tradable asset, including user-generated ones.
The general performance requirement [NFR-P-06](../SRS.md#34-performance) requires the API to be responsive even under
heavy load. If it takes the role of simulating the market in real-time, this requirement is under risk.
Also, a continuously running simulation in high granularity does not fit the expected behaviour of a stateless REST API
whose job is mainly to be a thin wrapper and access point to the database and other backend systems.

## Considered options

<!-- At least two options you really considered — not one invented afterwards to lose. -->

1. The API simulates market state, persists it completely in the database
2. A dedicated gameserver runs the simulation and persists every simulated tick in the database
3. A dedicated gameserver runs the simulation and only summaries are persisted

## Decision

<!-- One or two sentences: "We will …", and the main reason. -->

We will implement option 3, because a continuously running simulation would put a big load on the API, risking
performance requirements. Persisting only summaries instead of every price tick allows us to save storage space and
cost.

such as [NFR-P-06](../SRS.md#34-performance).
Secondly, extracting the simulation into a separate service allows us to implement a fine-grained simulation in
sub-second ticks that provides the frontend with highly realistic, real-time developments in volatile assets such as
crypto.

## Consequences

<!-- What gets better, and what gets worse. A record with only good consequences hides the price. -->

- Good: this approach is much more stable and scalable.
- Bad: initial setup and added infrastructure require more up-front work and more maintenance.
- After the setup and integration has happened, changing from this system is only sensible if both
    - prices for the dedicated hardware exceed reasonable limits and
    - computation requirement is far lower than expected

