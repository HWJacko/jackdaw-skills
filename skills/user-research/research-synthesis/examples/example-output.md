# Support Portal — Research Synthesis

Research question: what makes the publishing task difficult for these editors?
Scope: three fictional participants in one synthetic round. Recruitment and dates are unknown.
This round is separate from the earlier five-editor example. Do not combine the counts.

## Sources

| Evidence ID | Location | Study | Participant reference | Method and limits |
| --- | --- | --- | --- | --- |
| SPEV001 | input.md Session A | current round | P1 | session notes; recruitment unknown |
| SPEV002 | input.md Session B | current round | P2 | session notes; recruitment unknown |
| SPEV003 | input.md Session C | current round | P3 | session notes and supplied quote; recruitment unknown |

## Observations

| Observation ID | Participant | Observation or supplied quote | Form | Evidence ID and location |
| --- | --- | --- | --- | --- |
| SPOB001 | P1 | Asked a developer to confirm the page appearance after checking preview | paraphrase | SPEV001, first note |
| SPOB002 | P1 | Waited for an answer before continuing | paraphrase | SPEV001, second note |
| SPOB003 | P2 | Was uncertain whether preview reflected the live layout | paraphrase | SPEV002 |
| SPOB004 | P3 | Could not find Publish | paraphrase | SPEV003, first note |
| SPOB005 | P3 | The preview matched what I expected. | supplied quote | SPEV003, second note |

## Findings

| Finding ID | Interpretation | Supporting observations | Contrary observations | Distinct supporting participants | Limits |
| --- | --- | --- | --- | --- | --- |
| SPRF001 | Some participants lacked confidence about the preview | SPOB001, SPOB002, SPOB003 | SPOB005 shows a different experience | 2 of 3 | interpreted finding; repeated P1 notes count once; not population prevalence |
| SPRF002 | Finding the publishing action was difficult for one participant | SPOB004 | none supplied | 1 of 3 | interpreted finding; no claim about other editors |

## Proposed actions and questions

Investigate what produces the different preview experiences. Ask which publishing states the participants saw.
Check whether the action label or its location affected P3. These are proposed research actions, not agreed requirements.
No market prevalence, statistical significance, or product approval is established.

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
| SPEV001 | SPOB001 | source | recorded | input.md SPEV001 |
| SPEV001 | SPOB002 | source | recorded | input.md SPEV001 |
| SPEV002 | SPOB003 | source | recorded | input.md SPEV002 |
| SPEV003 | SPOB004 | source | recorded | input.md SPEV003 |
| SPEV003 | SPOB005 | source | recorded | input.md SPEV003 |
| SPOB001 | SPRF001 | supports | recorded | observation and finding tables |
| SPOB002 | SPRF001 | supports | recorded | observation and finding tables |
| SPOB003 | SPRF001 | supports | recorded | observation and finding tables |
| SPOB005 | SPRF001 | contrary | recorded | observation and finding tables |
| SPOB004 | SPRF002 | supports | recorded | observation and finding tables |
| SPRF001 | SPPR001 | may inform | proposed | proposed interpretation for the supplied problem |
| SPRF002 | SPPR001 | may inform | proposed | proposed interpretation for the supplied problem |

## Evidence map

Legend: source observations are observed. Findings are interpreted. The `contrary` edge preserves P3's different preview experience.
The map does not count notes as independent participants or show an agreed product decision.

```mermaid
flowchart LR
    SPEV001["SPEV001 Session A, P1<br/>source notes"]
    SPEV002["SPEV002 Session B, P2<br/>source notes"]
    SPEV003["SPEV003 Session C, P3<br/>source notes and quote"]
    SPOB001["SPOB001 Asked for layout confirmation<br/>observed; P1 paraphrase"]
    SPOB002["SPOB002 Waited for an answer<br/>observed; P1 paraphrase"]
    SPOB003["SPOB003 Unsure about preview<br/>observed; P2 paraphrase"]
    SPOB004["SPOB004 Could not find Publish<br/>observed; P3 paraphrase"]
    SPOB005["SPOB005 Preview matched expectations<br/>observed; P3 supplied quote"]
    SPRF001["SPRF001 Preview confidence varies<br/>interpreted; 2 of 3 supporting participants"]
    SPRF002["SPRF002 Finding Publish was difficult<br/>interpreted; 1 of 3 supporting participants"]
    SPEV001 -- "source" --> SPOB001
    SPEV001 -- "source" --> SPOB002
    SPEV002 -- "source" --> SPOB003
    SPEV003 -- "source" --> SPOB004
    SPEV003 -- "source" --> SPOB005
    SPOB001 -- "supports" --> SPRF001
    SPOB002 -- "supports" --> SPRF001
    SPOB003 -- "supports" --> SPRF001
    SPOB005 -- "contrary" --> SPRF001
    SPOB004 -- "supports" --> SPRF002
```
