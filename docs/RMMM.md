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
|   2   | Medium      | Medium |
|   3   | High        | High   |

Score = probability × impact.

**Our thresholds:** from H: act now · from M: plan · below that: watch

## Risks

<!-- One row per risk, sorted by score, highest first. Kind: project, technical or business.
     Status: open, occurred or closed. Updated: date of the last change. -->

| ID   | Risk, short                                  | Kind               | P | I | Score | Owner     | Status | Updated    |
|------|----------------------------------------------|--------------------|---|---|-------|-----------|--------|------------|
| R-01 | Overly ambitious goals endanger final result | Project Management | M | M | 4     | Sebastian | open   | 19.11.26   |
| R-02 | External service we depend on goes down      | Technical          | M | H | 6     | Max       | open   | 19.11.26   |
| R-03 | Exmatrikulation of one or more team Members  | Project            | M | H | 6     | Justus    | open   | 19.11.26   |

<!-- A risk with impact 5 that you do not write in full: one sentence here on what you would do if
     it occurred. -->

<!-- Copy the following block once for each risk you write in full. -->

### R-01 Too ambitious planning

*Owner: Sebastian*

**Risk.** Because multiple members of our group are quite excitable about building fun systems, we are at risk of
setting our goals much higher than strictly necessary, so that the implementation might take more time and resources
than we will eventually find out to have.

**Rating.** Probability 2 × impact 2 = 4. We already have experienced such tendencies in past meetings and are aware of
them. The impact would threaten the goals we set ourselves, but not the MVP which we expect to complete one semester
early.

**Mitigation.** We accept this risk, as our enthusiasm is the main driving factor behind our productivity. Deciding to
do the bare minimum would kill more motivation and make the project more arduous than overambition might harm our time
schedule.

**Indicator.** The backlog grows more than it reduces in size after each sprint in the second half of the fourth
semester.

**Contingency.** We will decouple a polished, presentable result for the lecture with overhauled documentation, while
fun projects can continue to be implemented on the main branch.

### R-02 External service we depend on goes down

*Owner: Max*

**Risk.** Because our demo runs entirely on services we do not control, Vercel for the frontend,
Supabase for database and auth, GitHub for code and CI, an external API for market data, and
PyPI/npm for our packages. One of them may be unavailable or unsafe to use when we need it (a provider
outage, a data centre lost to a flood, fire or war, cut internet cables, sanctions, or a critical
security flaw in Python or FastAPI), so we cannot show a working demo or cannot deploy for days.

**Rating.** Probability M (2) × impact H (3) = 6. Each single event is rare, but we depend on at least
five providers for two semesters, and large providers do have outages. If one hits the time of the presentation, we
have no demo.

**Mitigation.**
- Justus and Max add a local setup: `docker compose up` starts frontend and backend, `supabase start`
  starts a local Supabase with seed data; the steps go into the README.
- Dependencies are pinned in lock files.
- Every member keeps an up-to-date clone of the repository on their laptop.
- The day before the presentation, we record a short demo video as a last resort.

**Indicator.** A status page (GitHub, Vercel, Supabase, the market data API) reports an incident, or nobody has started the local setup successfully
during the last sprint.

**Contingency.**
1. Check the status pages to see which service is down.
2. Before a demo: pull from your local clone, run `supabase start` and `docker compose up`, and present from localhost.
3. For a security flaw: update to the patched version, if there is none yet, switch off the affected
   feature and say so in the demo.
4. If the local setup fails as well: play the demo video and explain the live parts.
5. Events that take away our laptops or the university as well (nuclear war) are accepted: then
   the demo is not our problem.

### R-03 Exmatrikulation of one or more team members

*Owner: Justus*

**Risk.** Because some of us still have to pass re-exams this semester, a member may be exmatrikuliert, so their open
user stories stay unfinished and nobody else knows that part of the code.

**Rating.** Probability 2 × impact 3 = 6. With the experience of the last semester, we know that this is a realistic
risk. Losing one person hurts, but the remaining members can still deliver a smaller product.

**Mitigation.** Accepted. Whether someone passes their exams is mostly outside the project’s control, so we do not plan
an extra measure for now.

**Indicator.** Failed exams or talking about exmatrikulation with the team.

**Contingency.** At the next sprint change, the owner and the team reassign the member's open stories to the remaining
members. If the work does not fit into the remaining sprints, we remove the lowest-priority stories from the backlog
first.