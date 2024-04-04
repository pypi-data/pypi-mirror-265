import webbrowser
from typing import List

import typer
from openai import OpenAI
from rich.prompt import Prompt
from typer_config import use_yaml_config
from typer_config.callbacks import argument_list_callback

from prrr.utils.git import get_current_branch, get_git_remote_url, read_last_commits

app = typer.Typer()


def default_template_file_exist():
    pass


def load_default_template_file():
    # if file exist read it and return its content else return empty
    # read
    filename = "template.md"
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Template file not found")
    return ''


@app.command("gen")
@use_yaml_config(default_value=".prr")
def pr_gen(
        open_browser: bool = typer.Option(default=False),
        prompt: bool = typer.Option(default=False),
        tone: str = typer.Option(default="friendly"),
        person: str = typer.Option(default="Donald Draper"),
        model: str = typer.Option(default="gpt-3.5-turbo"),
        instructions: List[str] = typer.Argument(default=None, callback=argument_list_callback),
        template: str = typer.Argument(default=None, callback=load_default_template_file),
):
    client = OpenAI(
        # Defaults to os.environ.get("OPENAI_API_KEY")
    )

    # print(instructions)

    # map instructions to messages
    instructions_messages = []
    for instruction in instructions:
        instructions_messages.append({"role": "system", "content": instruction})

    instructions_messages.append(
        {"role": "system", "content": "You are " + person + " and you are invested in this project."})

    context_messages = [
        {
            "role": "user",
            "content": "These are the commits I want you to use " + read_last_commits()},
        {
            "role": "system",
            "content": "Use the following template to organize and describe the changes: <template>" + template + "</template>"
        }, {
            "role": "system",
            "content": "Remember to use a " + tone + " tone."
        }]

    # prompt user for additional notes
    if prompt:
        while True:
            user_message = Prompt.ask("Additional notes (Press Enter to skip)")
            if user_message == "":
                break
            context_messages.append({"role": "user", "content": user_message})

    messages = [
        *instructions_messages,
        *context_messages
    ]

    # print(messages)

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    pr_body = chat_completion.choices[0].message.content
    print(pr_body)

    if open_browser:
        current_branch = get_current_branch()
        pr_url = get_git_remote_url() + '/compare/' + current_branch + '?&title=default&expand=1&body=' + pr_body
        webbrowser.open(pr_url, new=2)
