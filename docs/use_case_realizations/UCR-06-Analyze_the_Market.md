# UCR-06-Analyze_the_Market — Use-Case Realization

| Author    | Realizes                                                             |
|-----------|----------------------------------------------------------------------|
| Sebastian | [UC-06 Analyze the Market](../use_cases/UC-06_Analyze_the_Market.md) |

## 1 Introduction

This document describes the realization of [UC-06 Analyze the Market](../use_cases/UC-06_Analyze_the_Market.md).
It shows which objects work together, and in which order, when a user browses the asset list and opens the
details of one asset, or opens the details page directly (1a). The optional buy/sell action at step 5 is covered
as a reference to [UCR-05 Trade Assets](UCR-05-Trade_Assets.md), which realizes UC-05.

## 2 Flow of events — design

### 2.1 Participating objects

| Object         | Stereotype | Responsibility                                                                   |
|----------------|------------|----------------------------------------------------------------------------------|
| :AssetPage     | «boundary» | Shows the filterable asset list and the asset details page with Buy/Sell buttons |
| :AnalyzeMarket | «control»  | Loads the asset list, or one asset with its current price and history            |
| :Asset         | «entity»   | A tradable asset with its current price and historical price series              |

### 2.2 Sequence diagrams

![Sequence diagram UCR-06](../diagrams/UCR-06_sequence.png)

### 2.3 Walkthrough

The first `alt` swimlane describes the two ways how a player can reach the details page. In the `[browse list]` section ,
the user opens the asset list (step 1); `:AnalyzeMarket` loads all assets and the page shows them (filterable), and the user
selects one (step 3). In the `[direct link]` option (1a), the user opens an asset's details page directly, e.g.
from the portfolio, skipping the list.

Either way, `:AssetPage` then asks `:AnalyzeMarket` for that one asset's details; it loads the current price and
historical data from `:Asset` and the page shows it as charts (step 4).

The last `opt` fragment covers step 5: if the user clicks Buy or Sell, the trade itself is handled in UC-05
`Trade the Asset`.

### 2.4 State machine

Not applicable

## 3 Derived requirements

None
