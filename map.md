
**VisualGit**

- What do you want to do?
[1] Work in main
	[1] Local
		[1] Check local repos
		[2] Create a local repo {*git init*}
		[3] Commit in local {*git add . && git commit -m*}
	[2] Local to remote
		[1] Check remote repos
		[2] Connect local repo with remote {*git remote add origin repo_address.git*}
		[3] Push changes to remote {*git push -u orign main*}
		[4] **Commit & Push** {*gitt add . && git commit -m && git push -u origin main*}
	[3] Remote to local
		[1] Check remote repos
		[2] Clone remote repo to local {*git clone repo_address*}
		[3] Pull changes to local {*git pull*}
	[4] Manage repos
		[1] Delete local repo
		[2] Delete remote repo
[2] Work in branches
	[1] Local
		[1] Check local branches {*git branch*}
		[2] Create a local branch {*git branch branch_name*}
		[3] Go to branch {*git checkout branch_name*}
		[4] Go to main {*git checkout main*}
	[2] Local to remote
		[1] Check remote branches
		[4] Connect local branch with remote {*git remote add branch_name branch_address.git*}
		[5] Commit in local branch {*git add . && git commit -m*}
		[6] Push chanes to remote branch {*git push -u origin branch_name*}
		[7] **Commit & Push in branch** {*git add . && git commit -m && git push -u origin branch name*}
	[3] Manage branches
		[9] Merge branch with main
			- Si no estás en main: {*git checkout main && git merge branch_name*}
			- Si ya estás en main: {*git merge branch-name*}
		[10] Delete local branch
		[11] Delete remote branch
[2] Exit		
	
	