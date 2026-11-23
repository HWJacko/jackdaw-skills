# Shop Analytics — Schema Map [VISUAL]

Handoff: needs_confirmation
Runtime controls: not_assessed
Source: SA-schema-model.json, inspection date 2026-11-23.

Legend: solid = observed or confirmed; dashed = assumed. Status labels determine query approval.

```mermaid
flowchart LR
    SATB001["SATB001 main.customers<br/>tenant_id INTEGER PK1<br/>customer_id INTEGER PK2<br/>display_name TEXT"]
    SATB002["SATB002 main.orders<br/>tenant_id INTEGER PK1<br/>order_id INTEGER PK2<br/>customer_id INTEGER<br/>status TEXT<br/>total_minor INTEGER<br/>currency_code TEXT"]
    SATB003["SATB003 main.order_items<br/>tenant_id INTEGER PK1<br/>order_id INTEGER PK2<br/>line_number INTEGER PK3"]
    SATB003 -- "SARL001 observed | declared many-to-one | query use blocked<br/>(tenant_id, order_id) to (tenant_id, order_id)<br/>Questions: SAQ002, SAQ007" --> SATB002
    SATB002 -. "SARL002 assumed | candidate many-to-one | query use blocked<br/>(tenant_id, customer_id) to (tenant_id, customer_id)<br/>Questions: SAQ001, SAQ007" .-> SATB001
```

## Open questions and limits

Blocking questions: SAQ001, SAQ002, SAQ003, SAQ004, SAQ005, SAQ006, SAQ007.
Both relationships are blocked for query use. No SME answers have been supplied.
The source is supplied DDL. No live database or business rows were inspected.
Foreign key enforcement and historical data validity were not checked.
No objects or relationships were omitted. No rejected relationships exist in this model.
