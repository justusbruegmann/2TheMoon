# Risk List (RMMM)

*Project: 2TheMoon · Team: Sebastian, Mika, Justus, Max*

RMMM stands for Risk Mitigation, Monitoring and Management. This list is a living document: we
look at it at every sprint change and change the date of every row we touch.

## Our Scale

<!-- Your scale, your words. Lecture 10, slide 18 shows an example you may start from — change the
     words until all of you mean the same by each number. Five steps are usual; three work, too. -->

| Value | Probability | Impact |
|:-----:|-------------|--------|
|   1   | Low         | Low    |
|   2   | Medium      | Low    |
|   3   | High        | High   |

Score = probability × impact.

**Our thresholds:** from [score]: act now · from [score]: plan · below that: watch

## Risks

<!-- One row per risk, sorted by score, highest first. Kind: project, technical or business.
     Status: open, occurred or closed. Updated: date of the last change. -->

| ID   | Risk, short                                 | Kind      | P | I | Score | Owner  | Status | Updated    |
|------|---------------------------------------------|-----------|---|---|-------|--------|--------|------------|
| R-01 | [a few words]                               | technical |   |   |       | [name] | open   | [DD.MM.YY] |
| R-02 | [a few words]                               |           |   |   |       | [name] | open   | [DD.MM.YY] |
| R-03 | Exmatrikulation of one or more team Members | Project   | M | H | 6     | Justus | open   | 19.11.26   |

<!-- A risk with impact 5 that you do not write in full: one sentence here on what you would do if
     it occurred. -->

<!-- Copy the following block once for each risk you write in full. -->

### R-01 [Risk, short]

*Owner: [name]*

**Risk.** Because [cause — what is already true today], [event — what may happen], so [effect —
what it would cost us].

**Rating.** Probability [value] × impact [value] = [score]. [One sentence: why these numbers.]

**Mitigation.** [What we do before it happens, so that it becomes less likely or less harmful.
Or: accepted, because …]

**Indicator.** [The warning sign we watch for.]

**Contingency.** [Our plan B: what we do when it has happened anyway.]

### R-01 [Risk, short]

*Owner: [name]*

**Risk.** Because [cause — what is already true today], [event — what may happen], so [effect —
what it would cost us].

**Rating.** Probability [value] × impact [value] = [score]. [One sentence: why these numbers.]

**Mitigation.** [What we do before it happens, so that it becomes less likely or less harmful.
Or: accepted, because …]

**Indicator.** [The warning sign we watch for.]

**Contingency.** [Our plan B: what we do when it has happened anyway.]

### R-03 Exmatrikulation of one or more team members

*Owner: Justus*

**Risk.** Because some of us still have to pass re-exams this semester, a member may be exmatrikuliert, so their open user stories stay unfinished and nobody else knows that part of the code.

**Rating.** Probability 2 × impact 3 = 6. With the experience of the last semester, we know that this is a realistic risk. Losing one person hurts, but the remaining members can still deliver a smaller product.

**Mitigation.** Accepted. Whether someone passes their exams is mostly outside the project’s control, so we do not plan an extra measure for now.

**Indicator.** Failed exams or talking about exmatrikulation with the team.

**Contingency.** At the next sprint change, the owner and the team reassign the member's open stories to the remaining members. If the work does not fit into the remaining sprints, we remove the lowest-priority stories from the backlog first.