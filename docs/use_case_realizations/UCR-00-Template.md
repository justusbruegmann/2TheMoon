# UCR-[NN] [Verb object] — Use-Case Realization

<!--
HOW TO USE THIS TEMPLATE
- Copy this file per realization and name it UCR-[NN]_[name].md, with the number of its
  use case: UCR-02_book_a_room.md realizes UC-02.
- Replace every [placeholder] in square brackets.
- Stay at the analysis level from Lecture 4: boundary, control, and entity objects, no
  framework classes yet. Task 5 replaces them with your design classes.
- Delete these comments once the realization is done.
- Structure after the RUP template "Use-Case Realization Specification":
  https://cin.ufpe.br/~if682/RUP/webtmpl/templates/a_and_d/rup_ucrs.htm
  Section 2 is RUP's "Flow of Events — Design".
-->

| Author | Realizes |
| ------ | -------- |
| [first name] | [UC-NN Verb object](../use_cases/UC-[NN]_[name].md) — and link this file from there |

## 1 Introduction

<!-- Two or three sentences: which use case this realizes, which of its flows it covers, and
     what is left out. Terms belong in the SRS, not here. -->

[…]

## 2 Flow of events — design

### 2.1 Participating objects

<!-- Every object in your sequence diagrams, with one responsibility each.
     Boundary: between an actor and the system — one per actor and use case;
               an external system is reached through a boundary too.
     Control:  coordinates this use case — usually one.
     Entity:   information that must be stored. -->

| Object | Stereotype | Responsibility |
| ------ | ---------- | -------------- |
| [:BookingForm] | boundary | [Takes room and slot from the student, shows the result] |
| [:BookRoom] | control | [Checks the slot, creates the booking, starts the notification] |
| [:Booking] | entity | [Stores who booked which room for which slot] |

### 2.2 Sequence diagrams

<!-- The basic flow and the alternative flows: alt if a flow rejoins, break if it ends the use
     case, opt for an optional step, loop for a repeated one, ref for an included use case.
     One diagram is enough while it stays readable; otherwise one per flow.
     Commit the source file next to the image. -->

![Sequence diagram UCR-[NN]](../diagrams/UCR-[NN]_sequence.png)

### 2.3 Walkthrough

<!-- Walk through the diagrams in a few sentences: which object does what, in which order,
     and how the diagrams fit together. Refer to the steps of the use case (1, 2, 4a …). -->

[…]

### 2.4 State machine

<!-- Optional. Only if an entity in this realization has a status with rules, e.g., a booking
     that is confirmed, canceled, or expired. Otherwise write "Not applicable". -->

[Not applicable]

## 3 Derived requirements

<!-- Requirements the design adds and the implementation must handle, each with an ID that is
     unique in the whole SRS, e.g.,
     DR-02-01 — The slot check and the insert of the booking run in one transaction.
     DR-02-02 — The e-mails are sent asynchronously; a failed send is retried three times.
     Write "None" if there are none. -->

- [DR-NN-01 — …]
- [DR-NN-01 — …]