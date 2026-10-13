# UC-[NN] [Verb object]

<!--
HOW TO USE THIS TEMPLATE
- Copy this file per use case and name it UC-01_[name].md, UC-02_[name].md, …
- Replace every [placeholder] in square brackets.
- Name: verb plus object, one goal reached in one sitting ("Book a room", not "Click Save").
- Describe what the actor and the system exchange, not which button is clicked —
  the mockup shows the screen.
- Delete these comments once the use case is done.
- Structure after the RUP template "Use-Case Specification":
  https://cin.ufpe.br/~if682/RUP/webtmpl/templates/req/rup_ucspec.htm
-->

| Author | Estimate | User stories |
| ------ | -------- | ------------ |
| [first name] | [story points] | [#12, #13 — and write "Implements UC-NN" into each of these issues] |

## 1 Brief description

<!-- One paragraph: the purpose of the use case and the value for the actor. -->

[…]

## 2 Actors

- **Primary:** [role that starts the use case]
- **Secondary:** [system or role the use case needs, or "none"]

## 3 Mockup

<!-- A wireframe is enough. Show the key step of this use case. -->

![Mockup UC-[NN]](../mockups/UC-[NN]_[name].png)

## 4 Flow of events

### 4.1 Basic flow

<!-- The success case, 3 to 9 numbered steps (Cockburn). Actor and system take turns. -->

1. The [actor] […].
2. The system […].
3. The [actor] […].
4. The system […].

### 4.2 Alternative flows

<!-- Name the step where each flow branches off and where it continues or ends.
     Errors, cancellations, and conflicts between users belong here.
     If your diagram shows another use case extending this one («extend»), name the step
     where it can start: "Extension point: …". If this use case always uses another one
     («include»), write it into the step: "(includes UC-07)". -->

**[N]a · [short name].** At step [N], [condition]. The system […]. The flow continues at
step [M] / The use case ends.

### 4.3 Sequence diagram

<!-- The flow above over time: the actor, your frontend, your backend, your database.
     Show an alternative flow as an alt fragment where it matters.
     Commit the source file (PlantUML, draw.io, …) next to the image. -->

![Sequence diagram UC-[NN]](../diagrams/UC-[NN]_sequence.png)

## 5 Special requirements

<!-- Quality requirements for this use case only, each with an ID that is unique in the
     whole SRS, e.g.,
     NFR-P-02 — The confirmation shall appear within 1 s for 95 % of the bookings.
     System-wide ones go into SRS sections 3.2 to 3.5. Write "None" if there are none. -->

[…]

## 6 Preconditions

<!-- The state of the system before the use case can start, e.g., "The user is logged in." -->

- […]

## 7 Postconditions

<!-- The state of the system after the use case, e.g., "The booking is stored." -->

- […]
