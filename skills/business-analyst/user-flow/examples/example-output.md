# NW — User Flow: NWEP001 Self-service publishing

Legend: rounded = start/end, rectangle = action, diamond = decision.

```mermaid
flowchart TD
    start([Start]) --> login[Editor logs in to CMS]
    login --> create[Create page in editor]
    create --> valid{Title and body present?}
    valid -- No --> create
    valid -- Yes --> draft[Save as draft]
    draft --> preview[Show preview]
    preview --> publish[Editor clicks Publish]
    publish --> approval{Admin approves?}
    approval -- No --> draft
    approval -- Yes --> live[Page live on website]
    live --> done([End])
```

Assumption: the approval workflow is configured. If it is not, the publish step goes straight from preview to live.
