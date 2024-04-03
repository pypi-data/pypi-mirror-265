# TFSports Basic Setup

## SSH Setup

You can configure SSH from [this](https://docs.gitlab.com/ee/ssh/) Gitlab tutorial.

## Clone

### Recursive 
```bash
 git clone --recurse-submodules git@gitlab.com:mesainc/tfsports-ios.git
```
Obs: It will clone the project and all submodules

### Non recursive
```bash
 git clone git@gitlab.com:mesainc/tfsports-ios.git
 git submodule init
 git submodule update
```
Obs: The first line will clone only the project; the second and the third lines will clone the submodules too

Important: ***Always check if the module branch is pointing to the current branch in development. Example if the main module is pointing to "sprint-26", the submodule should also point to "sprint-26", if the branch does not exist, it should be created.***

## Branch

1. The branch that you will work in **needs** to be created from the sprint branch;
2. Default branch name: ***type/TS-{number-TS}***;
- *type* can be:
1. feature: new story;
2. bugfix or fix: bugfix happens in Production scheme, and fix happens in any scheme diffent of Production;
3. chore: refactor or settings changes in project.

- /TS-: is static
- {number-TS}: the number of US in Jira

So, for example, the branch name will be this way: 

```bash
feature/TS-0000
```

## Commits

The commits has default messages: ***[TS-{number-TS}] type: description***

So, for example, it will be this way: 
```bash
[TS-0000] feature: implemeting layout
````

For more information about commit and branch messages, you can consult [this](https://gist.github.com/joaozig/beef698739fb76f9fb5f227741509cf2) infos.

## Merge Request

First, make sure the branch you are working on is up to date with the sprint branch. If not, you will have to update it and resolve conflicts if it exists. After that, you can push your changes and ask someone else to review the merge request.

If you are the one doing the review, before clicking Merge, you need to click Modify Commit and delete the first line.

## Build scheme

For development, you must always use build scheme in Xcode as "development" and "staging". 

**Important:** Don't test using build scheme as "**Production**", 
if you need to simulate a bug that is happening in production scheme, you can run it in "**ProductionDebug**".

## M1 

If you're using Macbook with Apple Silicon (M1) and wish build the project with simulators you should follow this steps:

1. Quit Xcode;
2. Right-click on Terminal in Finder;
3. Get info;
4. Open with Rosetta
5. Open Xcode and run the project

**Important:** After finishing tests reset this configurations.

## Errors

If you try to run the project and the error *Command PhaseScriptExecution failed with a nonzero exit code* shows, you can follow this steps:

1. Open Build Phases in Xcode
2. Open Lint Run Script
3. Comment the second line.

**Important:** Don't commit this change, it only serves to remove the error.




