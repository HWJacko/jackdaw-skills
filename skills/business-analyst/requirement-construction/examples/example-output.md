# New Website — User Stories
Project ID: NW

## NWUS001
Source use case: NWUC001
As a content editor I want to be able to create a page in the CMS so that I can publish content without developer help

Scenario 1: Editor creates a valid page
Given I am logged in to the CMS with an editor account
When I open the page editor
And I enter a title and body content
Then the page is saved as a draft
And I see a preview of the page

AC1: A page cannot be saved without a title
AC2: The draft is visible only to CMS users, not to visitors
AC3: The preview matches the published layout
