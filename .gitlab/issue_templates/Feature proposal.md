### Release notes 

What is the problem and solution you're proposing? This content sets the overall vision for the feature and serves as the release notes that will populate in various places.

### Problem to solve

What problem do we solve? Try to define the who/what/why of the opportunity as a user story. For example, "As a (who), I want (what), so I can (why/value)."

### Intended users

Who will use this feature? If known, include any of the following: types of users (e.g. Developer), personas, or specific company roles (e.g. Release Manager). It's okay to write "Unknown" and fill this field in later.

### User experience goal

What is the single user experience workflow this problem addresses? 
For example, "The user should be able to use ... with ARG to <perform a specific task>"

### Proposal

How are we going to solve the problem? Try to include the user journey!

### Further details

Include use cases, benefits, goals, or any other details that will help us understand the problem better.

### Permissions and Security

What permissions are required to perform the described actions? Are they consistent with the existing permissions as documented for users, groups, and projects as appropriate? Is the proposed behavior consistent between the UI, API, and other access methods (e.g. email replies)?
Consider adding checkboxes and expectations of users with certain levels of membership https://docs.gitlab.com/ee/user/permissions.html
* [ ] Add expected impact to members with no access (0)
* [ ] Add expected impact to Guest (10) members
* [ ] Add expected impact to Reporter (20) members
* [ ] Add expected impact to Developer (30) members 
* [ ] Add expected impact to Maintainer (40) members
* [ ] Add expected impact to Owner (50) members

### Documentation

See the Feature Change Documentation Workflow https://automaticreportgenerator.gitlab.io/arg/

* Add all known Documentation Requirements in this section.
* If this feature requires changing permissions, update the permissions document.

### Availability & Testing

This section needs to be retained and filled in during the workflow planning breakdown phase of this feature proposal, if not earlier.

What risks does this change pose to our availability? How might it affect the quality of the product? What additional test coverage or changes to tests will be needed? Will it require cross-browser testing?

Please list the test areas (unit, integration and end-to-end) that needs to be added or updated to ensure that this feature will work as intended. Please use the list below as guidance.
* Unit test changes
* Integration test changes
* End-to-end test change

### What does success look like, and how can we measure that?

Define both the success metrics and acceptance criteria. Note that success metrics indicate the desired business outcomes, while acceptance criteria indicate when the solution is working correctly. If there is no way to measure success, link to an issue that will implement a way to measure this.

### Is this a cross-stage feature?

Communicate if this change will affect multiple Stage Groups or product areas. We recommend always start with the assumption that a feature request will have an impact into another Group. Loop in the most relevant PM and Product Designer from that Group to provide strategic support to help align the Group's broader plan and vision, as well as to avoid UX and technical debt.

### Links / references

Label reminders - you should have one of each of the following labels if you can figure out the correct ones
/label ~devops:: ~group: ~Category:

/label ~feature