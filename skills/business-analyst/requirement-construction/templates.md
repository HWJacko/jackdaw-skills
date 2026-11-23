# Templates — Requirement Construction

## Identifier

| Item | Format | Example |
| :--- | :--- | :--- |
| User story (local) | `[PN]US###` | `NWUS001` |

The local ID is not the JIRA key. A JIRA key is added later only if a JIRA connection is available.

Record `Source use case: [PN]UC###` under each story heading. Use `unknown` when the source has no ID.

## Story format

> As a [stakeholder] I want to be able to [action] so that [outcome]

## Scenario format (Gherkin)

```gherkin
Given [precondition]
When [action]
And [additional condition]
Then [expected result]
And [additional result]
```

Use AND / BUT / OR as needed. One scenario per distinct behaviour.

## Output skeleton

```markdown
## [PN]US001
Source use case: [PN]UC001
As a [stakeholder] I want to be able to [action] so that [outcome]

Scenario 1: [name]
Given ...
When ...
Then ...

AC1: ...
AC2: ...
```

## Canonical examples

### Example 1

> As an end user I want to be able to generate charts and graphs from files on request in regular Chat with Documents conversations, so I can better gain insights from data

Scenario 1: Chat with Docs context produces charts/graphs
Given I have selected a file to query against
When I prompt against the file
AND sufficient data is available for chart/graphs
Then charts and graphs are provided in the response from Elysia using the context that has been provided
And these should be accompanied with text that explains their significance

AC1: Charts and graphs should not be automatically delivered for all csv and xlsx files, only when sufficient data is available.
AC2: All files types can be used as a source of context for the charts/graphs.
AC3: This should work with multiple files selected
AC4: The conversation can be continued as normal after this point
AC5: The conversation does not become a Data Analytics discussion, it can be continued as a "normal" conversation.

### Example 2

> As an end user I want Elysia to list all of the sources used in gathering the response, so I can verify the detail.

Scenario 1: I run a query against a Global KB
Given I am in Elysia
When I ask a prompt that uses a Global KB document
AND the document has a source URL in its metadata
Then the response should include a Knowledge Base row in the source section
AND the source should be hyperlinked with the source url from the metadata
AND the source should show the DisplayName from the metadata
OR the File Name if no DisplayName is present

AC1: Sources without a source url are still used in context, but not listed
AC2: the number in the source for web or files reflects the number of items used as sources
AC3: the source section is closed by default
AC4: this is just for Global KBs, not shared KBs, or KBs created for API collections
