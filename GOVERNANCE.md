# STiX Shifter Governance *In Progress*

*Attribution: This template was created from the output of the Harbor Project team. See their excellent [GOVERNANCE.md file](https://github.com/goharbor/community/blob/master/GOVERNANCE.md) for what it looks like in action.*

This document defines the project's community governance per [OASIS Open Projects Governance Policy](https://github.com/oasis-open-projects/documentation/blob/master/policy/project-governance.md).

## Overview

STiX, an OASIS Open Project, is committed to building an open, inclusive, productive and self-governing open source community that creates next-generation APIs for cloud computing. The community is governed by this document and in accordance with [OASIS Open Project Rules](../board-docs/open-projects-rules.md) with the goal of defining how community should work together to achieve this goal.

## Code Repositories

* **[https://github.com/opencybersecurityalliance/stix-shifter]():** Main codebase.

## Community Roles

* **Contributors:** People who make regular contributions to our project (documentation, code reviews, responding to issues, participation in proposal discussions, contributing code, etc.).
* **Maintainers**: People who have been selected by project leadership to oversee one or more components of the project, review code and PRs, prepare releases, triage issues, and similar tasks.

## Project Leadership

* **Technical Steering Commitee**: ???
* **Change Control Board**: Group responsible for the overall technical health and direction of the project; final reviewers of PRs, responsible for releases, responsible for overseeing work of maintainers and community leaders.

### List of CCB Members

* Chair of CCB: 
* CCB Members:

### Joining the CCB

New maintainers must be nominated by an existing maintainer or CCB member and must be elected by a Special Majority of the Maintainers. Likewise, maintainers can be removed by a Special Majority of the total TSC or can resign by notifying the TSC.

## Decision Making

TSC/CCB Relations

### Special Majority Vote

Special Majority is a vote in which at least 2/3 (two thirds) of the eligible voters vote "yes" and no more than 1/4 (one fourth) of the eligible voters vote "no". These numbers are based on the total number of eligible voters in the committee. Abstentions are not counted. For example, in a Committee in which there are 30 Voting Members, at least 20 Voting Members must vote "yes" for a motion to pass; but if 8 or more vote "no" then the motion fails.

### Lazy Consensus

Out of respect for other contributors, major changes should also be accompanied by a ping on Slack or a note on the Harbor dev mailing list as appropriate. Author(s) of proposal, Pull Requests, issues, etc.  will give a time period of no less than five (5) working days for comment and remain cognizant of popular observed world holidays.
Other maintainers may chime in and request additional time for review, but should remain cognizant of blocking progress and abstain from delaying progress unless absolutely needed. The expectation is that blocking progress is accompanied by a guarantee to review and respond to the relevant action(s) (proposals, PRs, issues, etc.) in short order.
Lazy Consensus is practiced for all projects in our org, including the main project repository, community-driven sub-projects, and the community repo that includes proposals and governing documents.
Lazy consensus does _not_ apply to the process of:

* Removing maintainers
* Appointing CCB members
* Moving streams of work to a standards track

## Proposal Process

Large changes to the codebase and / or new features should be preceded by a proposal. This process allows for all members of the community to weigh in on the concept (including the technical details), share their comments, ideas, and use cases, and offer to help. It also ensures that members are not duplicating work or inadvertently stepping on toes by making large conflicting changes.
The project roadmap is defined by accepted proposals.

Proposals should cover the high-level objectives, use cases, and technical recommendations on how to implement. In general, the community member(s) interested in implementing the proposal should be either deeply engaged in the proposal process or be an author of the proposal.
The proposal should be documented as a separated markdown file pushed to the root of the `proposals` folder in the [community](https://github.com/goHarbor/community) repository via PR. The name of the file should follow the name pattern `<short meaningful words joined by '-'>_proposal.md`, e.g:`clear-old-tags-with-policies_proposal.md`.
Use the [Proposal Template]() as a starting point.

### Proposal Lifecycle

The proposal PR can be marked with different status labels to represent the status of the proposal:
* **New**: Proposal is just created.
* **Reviewing**: Proposal is under review and discussion.
* **Accepted**: Proposal is reviewed and accepted (either by consensus or vote).
* **Rejected**: Proposal is reviewed and rejected (either by consensus or vote).

### Issue Tagging:

> To be done

* Process
* Bug
* Question
* Request for Enhancement

### Release and Version Management

> To be done

## Updating Governance

All substantive changes in Governance require a vote of the TSC.
