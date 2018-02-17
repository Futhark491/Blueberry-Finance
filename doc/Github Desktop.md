# Github Desktop

## Setting up Github Desktop

1. Download [Github Desktop](https://desktop.github.com/)
2. Sign in with your Github account & configure Github Desktop as needed
3. File > Clone Repository
4. Select "Blueberry Finance" from the list of repositories you belong to
5. Click "Fetch Origin" (at the top right) to confirm that the repository is up to date.

## Code Editing Process

1. Swap to the desired branch
    1. To create a new branch, Go to Branch > New Branch, and type in the name of the branch to be created (make sure to "publish" the branch at the top right after creating it)
    2. To switch to an existing branch, select the "Current Branch" button at the top center of the screen and select the branch you want from the dropdown
        1. Please note that this process will automatically update all the files in the directory, so make sure there are no *uncommitted changes* in the repository before switching.
2. Edit code as needed
3. Commit code to branch often during the editing process
    1. **Test before committing**
    2. Confirm that you are in the correct branch
    3. Add a **descriptive** summary, and an optional description detailing the changes made
    4. Click "Commit to [selected branch]"
    5. "Push" changes to Github server with the button at the top right
4. Test your code thoroughly
5. Once your changes are ready to push to the master branch, go to Branch > Update from Default Branch
6. Resolve any merge conflicts that occur by manually updating the files in your branch
7. Commit any merge conflict fixes to your local branch
8. Repeat steps 4-7 until you merge the "default" branch into your branch without merge conflicts
9. Create a pull request by going to Branch > Create Pull Request (this will redirect you to the github website, where you will fill out a form to create a request)
10. Once Github confirms that the branches can be safely merged, you may do so