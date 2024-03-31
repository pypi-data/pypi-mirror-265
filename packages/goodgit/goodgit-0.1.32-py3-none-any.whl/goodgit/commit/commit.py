import re
import git
import json
import requests
import subprocess
import questionary
from halo import Halo
from rich import print

from .add import git_unadd
from goodgit.utils import is_git_repo

def get_git_diff():
    """
    Gets the git diff for the HEAD.
    
    Returns:
        str: The git diff output.
    """
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    return result.stdout


def highlight_keywords(text):
    """
    Highlights keywords enclosed in backticks within the text.
    
    Parameters:
        text (str): The text to highlight.
        
    Returns:
        str: The text with highlighted keywords.
    """
    return re.sub(r"`(.*?)`", "[bold white]\\1[/bold white]", text)

def commit():
    """
    Main function to handle the git commit operation.
    """
    repo = git.Repo(".")
    
    # Get the git diff
    git_diff = get_git_diff()

    if not repo.is_dirty():
        print("[green]All clean, Nothing to commit[/green]")
        return False
    
    spinner = Halo(text='Baking your commit', spinner='moon')
    
    spinner.start()
    
    
    # Prepare the payload for the API call
    payload = json.dumps({
        "git_diff": git_diff,
    })

    headersList = {
        "Accept": "*/*",
        "User-Agent": "GoodGit",
        "Content-Type": "application/json",
    }

    reqUrl = "https://api.goodgit.io/api/commit/"
    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    
    spinner.stop()

    # Handle the API response
    if response.status_code == 200:
        commit_json = response.json()
        print(f"[bold orange1]{highlight_keywords(commit_json['subject'])}[/bold orange1]")
        print(f"[white]{highlight_keywords(commit_json['description'])}[/white]")

        # New feature: Option to commit or edit the commit message in a single step
        commit_choice = questionary.select("Do you want to commit the changes?", choices=['Yes', 'No', 'Edit']).ask()

        if commit_choice == 'Yes':
            # Commit without editing
            result = subprocess.run(["git", "commit", "-m", commit_json['subject'], "-m", commit_json['description']], capture_output=True, text=True)
            if result.returncode != 0:
                git_unadd()
                print(f"[red]Commit failed: {result.stderr}[/red]")
                return False
            else:
                print("[bold green]Commit successful![/bold green]")
                return True

        elif commit_choice == 'Edit':
            # Users can edit the commit subject and description
            commit_subject = questionary.text("Edit commit subject:", default=commit_json['subject']).ask()
            commit_description = questionary.text("Edit commit description:", default=commit_json['description']).ask()

            # Proceed to commit with the edited message
            result = subprocess.run(["git", "commit", "-m", commit_subject, "-m", commit_description], capture_output=True, text=True)
            if result.returncode != 0:
                git_unadd()
                print(f"[red]Commit failed: {result.stderr}[/red]")
                return False
            else:
                print("[bold green]Commit successful![/bold green]")
                return True

        else:
            # Handle 'No' choice
            # New feature implementation: Additional options after 'No'
            further_choice = questionary.select(
                "Choose an option:",
                choices=['Do not commit', 'Regenerate commit message']
            ).ask()

            if further_choice == 'Do not commit':
                git_unadd()
                print("[yellow]Commit cancelled. All changes have been unstaged.[/yellow]")
                return False

            elif further_choice == 'Regenerate commit message':
                # Repeat the process to generate a new commit message
                return commit()  # Calling the commit function again

            else:
                git_unadd()
                print("[yellow]Commit cancelled. All changes have been unstaged.[/yellow]")
                return False

    else:
        print("[red]Error fetching commit data[/red]")
        return False

