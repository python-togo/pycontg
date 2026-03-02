# pycontg25

### How to contriute

#### If you don't have git on your machine, [ install it](https://docs.github.com/en/get-started/quickstart/set-up-git).

##### Fork this repository

Fork this repository by clicking on the fork button on the top of this page.
This will create a copy of this repository in your account.

#### Clone the repository

Now clone the forked repository to your machine. Go to your GitHub account, open the forked repository, click on the code button and then click the _copy to clipboard_ icon.

Open a terminal and run the following git command:

```
git clone "url you just copied"
```

where "url you just copied" (without the quotation marks) is the url to this repository (your fork of this project). See the previous steps to obtain the url.

For example:

```
git clone https://github.com/yourusername/pycontg25.git
```

where `yourusername` is your GitHub username. Here you're copying the contents of the LearningHub repository on GitHub to your computer.

#### Create a branch

Change to the repository directory on your computer (if you are not already there):

```
cd pycontg25
```

Now create a branch using the `git switch` command:

```
git switch -c your-new-branch-name
```

For example:

```
git switch -c speakers-section
```

#### Update your dotenv file .env
Check discord dev-technical and you'll find the content of the env file
Basically it'll loks like this:
```bash
SUPABASE_URL=http://xxxxxxxx.ip.project.com
SUPABASE_KEY="eyJ0eXxxxxxxxxxxxxxx"
```

#### Create your virtual environment (Python 3.11 or above), install requirements and run
```bash
# With requirements.txt
python3.11 -m venv pytg # to create virtual env
source pytg/bin/activate # for linux users
source pytg/Scripts/activate # fro windosw users
pip install -r requirements.txt
python app.py

# Or with uv
pip install uv
uv sync
uv run app.py
```
#### Make necessary changes and commit those changes

If you go to the project directory and execute the command `git status`, you'll see there are changes.

Add those changes to the branch you just created using the `git add` command:

```
git add _your file_ or git add . #for multiple files
```
Now commit those changes using the `git commit` command:

```
git commit -m "your relevant message that shows the change you have done"
```

#### Push changes to GitHub

Push your changes using the command `git push`:

```
git push -u origin your-branch-name
```

replacing `your-branch-name` with the name of the branch you created earlier.

#### Submit your changes for review

If you go to your repository on GitHub, you'll see a `Compare & pull request` button. Click on that button.  
Now submit the pull request.  
Soon, the team be merging all your changes into the main branch of this project. You will get a notification email once the changes have been merged.
