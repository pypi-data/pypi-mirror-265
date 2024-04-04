import yaml


def generate_config_file():
    file_name = ".prr"
    defaults = {
        "project_name": "My Project",
        "project_description": "This is a project description",
        "model": "gpt-3.5-turbo",
        "tone": "friendly",  # friendly, professional, or casual
        "person": "senior software engineer",
        "template": "Template begins here: ```markdown" + "\n" +
                    "### Description" + "\n" +
                    "Describe the changes you've made in this pull request." + "\n" +
                    "### Benefits" + "\n" +
                    "Explain the benefits of these changes." + "\n" +
                    "### Testing" + "\n" +
                    "Explain how reviewers can test these changes." + "\n" +
                    "### Checklist" + "\n" +
                    "- [ ] I have read the CONTRIBUTING.md file." + "\n" +
                    "- [ ] I have tested the changes in this pull request." + "\n" +
                    "- [ ] I have updated the documentation." + "\n" +
                    "- [ ] I have added tests to cover my changes." + "\n" +
                    "### Additional Information" + "\n" +
                    "Add any additional information here. ```" + "\n" +
                    "Template ends here.",
        "instructions": [
            "You are a brilliant, meticulous and a great communicator engineer co-authoring a pull request. "
            "I will provide you with the description of the changes, the benefits, and the changelog. "
            "I want you to help me redact this pull request body in a way is clear, concise, and informative.",
            'Feel free to add any additional information you think is relevant.',
            "Print the markdown result without recommendations nor comments."
        ]
    }
    yaml_string = yaml.dump(defaults)
    with open(file_name, "w") as f:
        f.write(yaml_string)
