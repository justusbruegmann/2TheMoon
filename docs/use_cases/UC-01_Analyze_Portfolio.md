# UC-01 Analyze Portfolio

| Author | Estimate | User stories |
|--------|----------|--------------|
| Justus | 20       | 2TM-57       |

Realization: [UCR-01](../use_case_realizations/UCR-01-Analyze_Portfolio.md)

## 1 Brief description

The user wants to look at his portfolio and check the performance of his trades.
Furthermore, the stocks that this user holds will be displayed with the option to sell.

## 2 Actors

- **Primary:** User
- **Secondary:** System

## 3 Mockup

![Image](../mockups/Portfolio.png)

## 4 Flow of events

### 4.1 Basic flow

1. The user opens the portfolio page.
2. The System loads the investor's holdings and current prices and displays each stock with its quantity, current value
   and performance.
3. The System displays the holdings with the current prices

### 4.2 Alternative flows

**2a · No Holdings .** At step 2, user has no holdings. The system displays everything with "0" placeholders and
skeletons. The use case ends.

**2b · Price data unavailable.** At step 2, current prices cannot be retrieved. The system shows the last known prices
with a warning.

### 4.3 Sequence diagram

![](../diagrams/UC-01-Sequence.png)

### 4.4 Activity diagram


![Activity diagram UC-01](../diagrams/UC-01-activity.png)


## 5 Special requirements

| ID       | Requirement                                                                                    | Author |
|----------|------------------------------------------------------------------------------------------------|--------|
| NFR-U-01 | The portfolio shall show all the portfolio information without scrolling on a 1920x1080 screen | Justus |
| NFR-R-01 | If the api is not reachable the frontend shall show a error in less than 5s                    | Justus |
| NFR-P-01 | The api shall return data in less than 2s on p95 with 50req/s over 5min                        | Justus |
| NFR-S-01 | The frontend won't need any editing for adding new assets                                      | Justus |

## 6 Preconditions

- User is Logged in

## 7 Postconditions

Not applicable
