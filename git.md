# Git cheat sheet

## References

[Git GUIs](https://git-scm.com/downloads/guis)

[Git docs](https://git-scm.com/docs)

## Installation & Setup

### Hints for windows

[Git installer for windows](https://git-scm.com/download/win)
* Default editor used by git -> VSCode or something else than Vim

### Git global config file

Exists in either `~/.gitconfig` or `~/.config/git/config`.
The content applies to all git repos for the given user.

### Git configuration commands

[git config docs](https://git-scm.com/docs/git-config)

#### Get git version

```bash
git --version
```

#### List all config values

```bash
git config --list
```

#### Display git config values

```bash
git config user.name
git config user.email
```

#### Set git config values

```bash
git config --global user.name "<NAME>"
git config --global user.email some@email.com
```

#### Set default editor

- [setting editors commands](https://git-scm.com/book/en/v2/Appendix-C%3A-Git-Commands-Setup-and-Config)

    Example: Set VSCode as a default editor. Note that it requires `code` installed in `path`.

    ```bash
    git config --global core.editor "code --wait"
    ```

#### Editing whole config file

```bash
git config --global -e
```

##### Config to set up tools for VSCode

```ini
[core]
editor = code --wait
[diff]
tool = vscode
[difftool "vscode"]
cmd = code --wait --diff $LOCAL $REMOTE
[merge]
tool = vscode
[mergetool "vscode"]
cmd = code --wait $MERGED
```

#### Aliases

We can set up Git aliases to make our Git experience a bit simpler and faster.

Example:

```ini
[alias]
    s = status
    l = log
```

From command line

```bash
git config --global alias.s = status
```

#### Local config file

Local configuration is stored in `.git/config`. It applies only to the particular repo.

In order to update the local config we use the `--local` flag.

```bash
git config --local user.email "fake@email.com"
```

> This will overwrite the email global setting just for this repo.

### Ignoring changes

Use the `.gitignore` file to not track changes of working directory content.

[git ignore docs](https://git-scm.com/docs/gitignore)

[Github ignore docs](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)

[.gitignore generator](https://www.toptal.com/developers/gitignore) -  just type the language the project uses, like `rust`

Example: Ignore files with `log` extension

```text
*.log
```

Example: Ignore whole directory. Note `/`says it's a directory, not a file.

```text
<DIRNAME>/
```

Example: Ignore exact file

```text
secrets.txt
```

## Repo structure

### refs folder

In `.git\refs\heads` folder we have files per each branch head pointing to a commit.

In `.git\refs\remotes` folder we have files per each remote branch head pointing to a commit.

### HEAD file

In `.git/HEAD` file we have a reference to the HEAD of the current branch. But if we are in detached mode then the file consists of the commit sha.

### Objects folder

The `.git\objects` folder is where Git stores the backups of files, the commits in a repo, and more. The files are compressed and encrypted.

- commits

    Git commits objects combine a tree object along with the information about the context that led to the current tree. Commits store a reference to a parent commit(s), the author, the committer, and the commit message.

- trees

    Git trees are the objects used to store the contents of a directory. Each tree contains pointers that can refer to blobs and to other trees. Each entry in a tree contains the SHA-1 hash of a blob or tree, as well as the mode, type, and filename.

- blobs

    Git blobs are the binary large objects which Git uses to store the contents of files in a given directory. Blobs don't even include the filenames of each file or any other data. They just store the contents of a file.

#### Print the type of git object

```bash
git cat-file -t <SHA>
```

#### Print the content of git object

```bash
git cat-file -p <SHA>
```

## General

### HEAD

Is a pointer that refers to the current "location" in repository. TLDR it points to the last commit on a given branch.

### Untracked files

Untracked files are the files that are not staged/committed to any branch. They follow with the user no matter what the branch is.

## Git commands

### Initialize a new repository

[git init docs](https://git-scm.com/docs/git-init)

```bash
git init
```

- `.git` is a repository itself

### Add files to staging area

[git add docs](https://git-scm.com/docs/git-add)

```bash
git add <file1> <file2>
```

 - add all changes in working directory (incl. not tracked)

    ```bash
    git add .
    ```

- add only tracked but unstaged changes

    ```bash
    git add -u
    ```

### Commit files to repository

[git commit docs](https://git-scm.com/docs/git-commit)

```bash
git commit
```

- with  inline message

    ```bash
    git commit -m "bla bla"
    ```

- Redo a commit - add changes to previous commit with msg change

    ```bash
    git commit --amend
    ```

- Redo a commit - add changes to previous commit without editing msg

    ```bash
    git commit --amend --no-edit
    ```

### Read git history

[git log docs](https://git-scm.com/docs/git-log)

```bash
git log
```

- git log in convenient readable version

    ```bash
    git log --oneline
    ```

- git log only commits sha

    ```bash
    git log --format=format:%H
    ```

- Read a commit details with diffs

    ```bash
    git show <commit_sha>
    ```

### Git branch

[git branch docs](https://git-scm.com/docs/git-branch)

- create a new branch

    ```bash
    git branch <new-branch-name>
    ```

    > It is important from which branch we create a new branch as this is the starting point.

- display branches

    ```bash
    git branch
    ```

- display branches with last commits

    ```bash
    git branch -v
    ```

### Switching branches - `git switch` vs `git checkout`

[git checkout docs](https://git-scm.com/docs/git-checkout)

[git switch docs](https://git-scm.com/docs/git-switch)

- checkout does more things than switch, switch is for switching the branch only, while checkout is also for restoring working tree files

- checkout to the branch

    ```bash
    git checkout <branch-name>
    ```

- switch to the branch

    ```bash
    git switch <branch-name>
    ```

- create branch and checkout

    ```bash
    git checkout -b <new-branch-name>
    ```

- create branch and switch

    ```bash
    git switch -c <new-branch-name>
    ```

- switch to previous branch

    ```bash
    git switch -
    ```

- create a branch from other branch

    ```bash
    git checkout -b <new-branch> <old-branch>
    ```

- switch (and create if not present locally) to a branch which should track a remote branch

    This is useful if there is a new remote branch which has no branch locally to track the remote

    ```bash
    git switch <remote-branch-name-without-origin-prefix>
    ```

    > So if there is an `origin\something` remote branch, if we use `git switch something`, this will create a branch locally that tracks the remote `origin\something` branch.

    > The old way of doing it was `git checkout --track origin/something`

### Deleting branch

To delete a branch no matter what the merge status is, execute the following from other branch, like master

```bash
git branch -D <branch-to-delete>
```

### Rename branch

To rename a branch execute the following from the branch ou want to rename

```bash
git branch -m <new-name>
```

### Merge branch

[git merge docs](https://git-scm.com/docs/git-merge)

#### Fast-forward merge

When being on master branch we can merge changes from the feature branch using:

```bash
@master$ git merge <feature-branch>
```

> In the effect, the HEAD of master moves to the last commit on the feature branch. It will take all the commits from the feature branch. This works when there are no new commits on master branch after the feature branch was created. Also it does not create a merge commit, and just moves the HEAD to the last commit from the feature branch.

We can prohibit from fast forwarding by using a flag

```bash
git merge --no-ff <feature-branch>
```

> In the effect it enforces creation of a merge commit.

#### Merge conflicts

When merge conflicts are solved, remember about committing the changes. Then we can push ton origin.

Every `git pull` is actually also a `merge` which may consist of conflicting parts of code.

### Git cherry-pick

[Git cherry-pick docs](https://git-scm.com/docs/git-cherry-pick)

Git `cherry-pick` is a powerful command that enables arbitrary Git commits to be picked by reference and appended to the current working HEAD. Cherry picking is the act of picking a commit from a branch and applying it to another. git `cherry-pick` can be useful for undoing changes. For example, say a commit is accidentally made to the wrong branch. You can switch to the correct branch and `cherry-pick` the commit to where it should belong.

```bash
git cherry-pick <commit_sha>
```

### Git diff

[git diff docs](https://git-scm.com/docs/git-diff)

- display `unstaged` (working directory) changes

    If changes are not staged, then the command shows nothing.

    ```bash
    git diff [file_name]
    ```

- display `staged` and `unstaged`

    Display all changes `staged` and `unstaged` since `HEAD`

    ```bash
    git diff HEAD
    ```

- display `staged` changes

    ```bash
    git diff --staged [file_name]
    ```

- compare branches

    ```bash
    git diff branch_1..branch_2
    ```

- compare commits

    ```bash
    git diff commit_1..commit_2
    ```

    > We can compare different commits files using a `gui`, by selecting two commits while holding a `shift`

    > Instead of specifying commits we can use notation like `HEAD` (current commit) `HEAD~1` (current commit - 1)

### Git stash

[git stash docs](https://git-scm.com/docs/git-stash)

- Hide changes for future use

    When we want to switch branch but:

    - the changes on the current branch are `unstaged` or `staged` and would be overwritten by the version that exists on the other branch

    - there is a change on the current branch which we don't want to take to the other branch

    Then we use stashing (hiding for future use)

    ```bash
    git stash
    ```

    > Note that `git stash` is a shortcut for `git stash save`

    - To stash with a label that describes the stash

        ```bash
        git stash save <LABEL>
        ```

- Apply changes from last stash to working copy (removing from stash)

    ```bash
    git stash pop
    ```

    > Note this removes the most recently stashed change from stash

    - To apply stash based on the label

        ```bash
        git stash apply stash^{/<LABEL>}
        ```

- Apply changes from last stash to working copy

    ```bash
    git stash apply [stash@{id}]
    ```

    > Note this does not remove the recently stashed change from stash

    > Note that we may use the stash id to be used `stash@{id}`

- List stashes

    ```bash
    git stash list
    ```

- Drop stashes

    ```bash
    git stash drop [stash@{id}]
    ```

- Drop all stashes

    ```bash
    git stash clear
    ```

### Go to commit (jump back in time)

[git checkout docs](https://git-scm.com/docs/git-checkout)

Going to a specific commit

```bash
git checkout <commit-hash>
```

> Note this will lead to the `Detached HEAD`. This means that the HEAD points to this specific commit, while branch points to the last commit on branch.

### Detached HEAD

Usually, HEAD points to a specific branch reference rather than a particular commit. The branch reference is a pointer to the last commit made on a particular branch.

### Re-attaching detached HEAD

- switch to the old branch

    ```bash
    git switch <branch>
    ```

- switch to the new branch

    ```bash
    git switch -c <branch>
    ```

### Discarding changes in files

#### Git checkout

- reverting file version to HEAD

    ```bash
    git checkout HEAD <file>
    ```

    or

    ```bash
    git checkout -- <file>
    ```

#### Git restore

[git restore docs](https://git-scm.com/docs/git-restore)

- reverting file version to HEAD

    ```bash
    git restore <file>
    ```

- reverting file to a specific version

    ```bash
    git restore --source <commit> <file>
    ```

### Unstaging files

To not include the file in the commit we can unstage the file from staging area

```bash
git restore --staged <file>
```

To unstage the whole directory

```bash
git reset <dir>
```

or:

```bash
git restore --staged <dir>
```

### Undoing commits

[git reset docs](https://git-scm.com/docs/git-reset)

To undo commits on the branch and reset repo back to a specific commit. Commits are gone.

- Commits are gone and changes in files stay as unstaged

    ```bash
    git reset <commit>
    ```

- Commits are gone and changes in files are gone

    ```bash
    git reset --hard <commit>
    ```

### Reverting commits

[git revert docs](https://git-scm.com/docs/git-revert)

While `git reset` actually moves the branch pointer backwards eliminating commits, the `git revert` creates a new commit which reverses/undos the changes from a commit. We should use it when we want to reverse commits that other people already have on their machines.

```bash
git revert <commit>
```

> Note, we will be prompted to provide description to the new commit

### Cleaning up the repo from untracked files

[git clean docs](https://git-scm.com/docs/git-clean)

Cleans the working tree by recursively removing files that are not under version control, starting from the current directory.

```bash
git clean -f
```

### Pushing change

[git push docs](https://git-scm.com/docs/git-push)

- Pushing to remote branch

    ```bash
    git push <remote> <branch>
    ```

    > Usually just `git push` or `git push origin master`

- Pushing to a different branch

    ```bash
    git push <remote> <local-branch>:<remote-branch>
    ```

    example:

    ```bash
    git push origin pancake:waffle
    ```

    > Push local pancake branch to remote waffle branch. This is doable. Usually remote branch name is same as the local, but pushing to different one is totally possible.

- Pushing with the `-u` option, to set an upstream branch for our local one. After this, we can just `git push`

    ```bash
    git push -u origin master
    ```

    > It is an equivalent of `git push --set-upstream origin master.`

### Cloning repository

[git clone docs](https://git-scm.com/docs/git-clone)

```bash
git clone <url>
```

> Note, when cloning only the default branch is present locally as it is automatically tracking the remote one

### Git submodules

[submodules docs](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

When we want to share libraries instead of use package managers. It gives access to the complete library.

- Adding a submodule

    ```bash
    git submodule add <URL>
    ```

Git keeps track of submodules in `.gitmodules` file.

Git command on the repo ignore the submodules unless we explicitly say that the command should include submodules.

We can configure including submodules by default with:

```bash
git config submodule.recurse true
```

> This will add the `--recurse-submodules` to all commands

- Pull the main repo with submodules

    ```bash
    git pull --recurse-submodules
    ```

- Clone the main repo with submodules

    ```bash
    git clone <URL> --recurse-submodules
    ```

- If the repo was cloned without the `--recurse-submodules` flag

    ```bash
    git submodule update --init
    ```

- Update submdules and initialize if necessary

    ```bash
    git submodule update --init --recursive
    ```

### Git fetch

[git fetch docs](https://git-scm.com/docs/git-fetch)

Fetching downloads the changes from a remote repository, without automatic integration to our working files.
It lets us see what other were working on but without merging the changes to our local repo.
If we don't fetch, our local repo has no idea about changes made on o `origin`. So `git status` would show nothing.
However after `git fetch`, the `git status` would show that local branch is behind the `origin`.

- Fetching remote branch changes

    ```bash
    git fetch <remote>
    ```

- Usually remote defaults to `origin` so most of the times this will be just

    ```bash
    git fetch
    ```

    > Note, it will fetch all the changes

- Fetch changes only from one branch

    ```bash
    git fetch origin <branch-name>
    ```

    > Note, it will create an `origin/<branch-name>` branch locally while keeping local `<branch-name>` unchanged.

### Git pull

[git pull docs](https://git-scm.com/docs/git-pull)

Pull changes from remote and update my local repo. It updates the HEAD.
So actually `git pull` = `git fetch` + `git merge`.

```bash
git pull <remote> <branch>
```

### Rebasing

[git rebase docs](https://git-scm.com/docs/git-rebase)

The `git rebase` command is used:
- as an alternative to merging
- as a cleanup tool (clean up your own commits, clean up your git history)

#### Alternative to merging

`rebase` and `merge` both help to combine changes from two branches

Rebase is helpful to keep the commits history clean where while working on feature branch many changes happen on master. We could constantly merge new changes but this would require us to have multiple merge commits on a feature branch which do not bring much value and make the history cluttered. Rebasing in this case rewrites the history by creating new commits for the feature branch and move the start of the feature branch to the tip of the of the master branch. So the rebase gives us a new base for feature branch.

```bash
git rebase master
```

While rebasing conflicts may appear. So we should resolve them add (stage) changes (but not commit them) and use:

```bash
git rebase --continue
```

When not to rebase

Never rebase commits that have been shared with others. Cause you ma change the history for people that have different history. Never rebase the master branch.

#### Rewriting history

We can use `git rebase` when we want to rewrite, delete, rename or reorder commits before sharing them.

Entering the interactive rebase

```bash
git rebase -i HEAD~<NUMBER OF COMMITS BACK FROM HEAD>
```

This will open a text editor with the following:

```text
pick <SHA1> <COMMIT1 MSG>
pick <SHA2> <COMMIT2 MSG>
pick <SHA3> <COMMIT3 MSG>
```

> Note the order is opposite to `git log`

##### Reword

So now if we want to reword the `<COMMIT1 MSG>` we use:

```text
reword <SHA1> <COMMIT1 MSG>
```

And we close the edited file. The editor will open a file where the message is so that we can change it.

> Note this changes SHA for all the commits starting from the one edited.

##### Fixup

Use commit contents but meld it into previous commit and discard the commit message

So if we have the following

```text
pick <SHA1> <COMMIT1 MSG>
fixup <SHA2> <COMMIT2 MSG>
pick <SHA3> <COMMIT3 MSG>
```

We will get

```text
pick <SHA1> <COMMIT1 MSG> <-- here will be the content of commits 1 and 2, but commit 1 msg
pick <SHA3> <COMMIT3 MSG>
```

##### Drop

Using drop will remove the commit completely.

### Reflog

[git reflog docs](https://git-scm.com/docs/git-reflog)

Git keeps a record of when the tips of branches and other references were updated in the repo. We can view and update these reference logs using the `git reflog` command.
For example we can find the `HEAD` file which actually shows the history of `HEAD`. Every time we do something it is being recorded.

Logs are kept in `.git\logs` folder.

Only local activity logs are kept. They are kept up to 90 days.

- Show reflog (it defaults to HEAD)

    ```bash
    git reflog show
    ```

    > We can pass a reference of branch or a HEAD, like `git reflog show master`

- Reflog references

    ```text
    name@{qualifier}
    ```

    > Like HEAD@{2} - means where the HEAD was 2 moves/entries ago, either commits or switch branches etc. Do not confuse with HEAD~2 what means 2 commits ago.

- Timed references

Every entry in the reference logs has a timestamp associated with it. We can filter reflogs entries by time/date by using time qualifiers like:

```text
1.day.ago
3.minutes.ago
yesterday
Fri, 03 Nov 2023 14:06:21-0800
```

## Github

A hosting platform for git repositories.

### SSH Key

You need to be authenticated on Github to do certain operations, like pushing up code from local machine. The terminal will prompt every single time for Github email and password unless we generate and configure an SSH key.

[Github SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

Note that steps below depend on the system used.

[Searching for existing SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)

```bash
ls -al ~/.ssh
```

[Generating new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

> Check if the file was created in the `.ssh` directory
> If prompted for providing the file name use downstream `<name>.pub` instead of default `id_ed25519.pub`

[Adding SSH key to github account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

```bash
clip < ~/.ssh/id_ed25519.pub
```

> Then add the copied SSH key to the `github`

- To read remote repository url

    ```bash
    git remote -v
    ```

> Note for HTTPS `https://github.com/<owner>/<repo_name>.git`, for SSH `git@github.com:<owner>/<repo_name>.git`

- To change the existing remote

    ```bash
    git remote set-url origin <url>
    ```

### Credentials

- Check where credentials are stored for HTTP

    ```bash
    git config credential.helper
    ```

> If returns `manager`, `manager-core` this means that the password is stored in windows credential manager.

> If returns `store``, password is stored in a .git-credentials file in the user folder.

### Binding local repo with remote repo

This is in case a local repo was created before the remote one was created.

- Create a new empty repo on github
- Connect local repo (add remote)

    - Check the current remote

        ```bash
        git remote -v
        ```

    - Add remote

        ```bash
        git remote add <name> <url>
        ```

        > The `<name>` usually is `origin`. It is conventional Git remote name

- Push

See the push section

### Remote branches

The naming convention is <remote-name>/<remote-branch-name>. Example `origin/master`.

- To display all remote branches we use

    ```bash
    git branch -r
    ```

### README

When put in the root of the git repository, it will be rendered and displayed by the github automatically.

Should consist of:

- what the project does
- how to run the project
- why it's noteworthy
- who maintains the project

Useful links:
- [markdown-it](https://markdown-it.github.io/)
- [markdown docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

### Pull request, Merge request

A Git `pull request` is essentially the same as a Git `merge request`. Both requests achieve the same result: merging a developer's branch with the project's master or main branch. Their difference lies in which site they are used; `GitHub` uses the Git `pull request`, and `GitLab` uses the Git `merge request`.

### Branch protection rules

[github branch protection docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

### Forking

Creation of own version of someones repository on GitHub or other hosting services.

After making changes to fork, we can make a `pull request` to merge fork changes to the remote.

The fork & clone workflow allows to push into `fork`, and to pull from the `remote` (as the contributors might have delivered something I don't have on my own fork). In order to be able to pull for changes we have to add the `remote` as `upstream`.

- Check remote repositories

    ```bash
    git remote -v
    ```

    > We can see the `origin`

- Add the `upstream`

    ```bash
    git remote add upstream <remote url>
    ```

- Check remote repositories

    ```bash
    git remote -v
    ```

    > We can see the `origin` and `upstream`

- Pull changes from `remote`

    ```bash
    git pull upstream main
    ```

The reason for this flow to exist is that it allows a project maintainer to accept contributions from developers all around the world wthout having to add them as actual owners of the main project repository or worry about giving them all permission to push to the repo.

### Tags

Tags are pointers that refer to particular points in Git history. Tags are most often used to mark releases in projects. They are branch references that do not change. Once a tag is created, it always refers to the same commit. It is just a label for a commit.

- Semantic versioning

    `<MAJOR>.<MINOR>.<PATCH>`

    `MAJOR` - significant changes that is no longer backwards compatible. Features may be removed or changed substantially

    `MINOR` - new features or functionality have been added, but the project is stil backwards compatible. The new functionality is optional and should not force users to rewrite their own code

    `PATCH` - no new features, no breaking changes (usually bug fixes), so it does not impact how people use the software

- View the list of all the tags

    ```bash
    git tag
    ```

- Display the current tag

    ```bash
    git describe --tags
    ```

- View the tags that match a pattern

    ```bash
    git tag -l "<pattern>"
    ```

    > Example: `git tag -l "*beta*"` will print a list of all tags that include "beta" in their name

- Checkout tag (checkout to the tagged commit, detached state)

    ```bash
    git checkout <tag>
    ```

- Checkout tag to new branch

    ```bash
    git checkout [tags/]<tag> -b <branch>
    ```

    > Note, `tags/` is optional

- Diff between tags

    ```bash
    git diff <tag1> <tag2>
    ```

- Create lightweight tag

    ```bash
    git tag <tagname>
    ```

    > it binds the tag to the current HEAD

- Create annotated tag

    ```bash
    git tag -a <tagname>
    ```

    > Editor will prompt for more info in tag message

    ```bash
    git tag -a <tagname> -m"message"
    ```

- Read specifics of tag including message

    ```bash
    git show <tagname>
    ```

- Tag previous commit

    ```bash
    git tag <tagname> <commit>
    ```

- Replace tag (change the commit it tags)

    ```bash
    git tag -f <tagname> <commit>
    ```

    > Tag is moved from one tag to the other

- Delete tag

    ```bash
    git tag -d <tagname>
    ```

- Pushing tags (Tags are not pushed with the code)

    To push all tags to remote

    ```bash
    git push --tags
    ```

    To push a particular tag to remote

    ```bash
    git push origin <tagname>
    ```
