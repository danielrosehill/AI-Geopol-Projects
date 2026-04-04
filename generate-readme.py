#!/usr/bin/env python3
"""
Generate README.md from projects.json for AI Geopolitical Projects.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_projects_data(filepath: Path) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_shields_badge(repo_url: str) -> str:
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]
    return f"![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social) ![GitHub last commit](https://img.shields.io/github/last-commit/{owner}/{repo})"


def generate_project_section(project: dict) -> str:
    output = []
    output.append(f"## [{project['name']}]({project['repository']})")
    output.append("")
    badges = generate_shields_badge(project['repository'])
    output.append(badges)
    output.append("")
    output.append(project['description'])
    output.append("")
    if project.get('features') and len(project['features']) > 0:
        output.append("**Features:**")
        for feature in project['features']:
            output.append(f"- {feature}")
        output.append("")
    if project.get('data_sources') and len(project['data_sources']) > 0:
        output.append(f"**Data Sources:** {', '.join(project['data_sources'])}")
        output.append("")
    if project.get('language') and project['language'] != 'unknown':
        output.append(f"**Language:** {project['language'].title()}")
        output.append("")
    if project.get('author'):
        author_link = f"[{project['author']}]({project['author_url']})" if project.get('author_url') else project['author']
        output.append(f"**Author:** {author_link}")
        output.append("")
    if project.get('demo'):
        output.append(f"**Demo:** [{project['demo']}]({project['demo']})")
        output.append("")
    if project.get('homepage'):
        output.append(f"**Website:** [{project['homepage']}]({project['homepage']})")
        output.append("")
    if project.get('notes'):
        output.append(f"*{project['notes']}*")
        output.append("")
    output.append("---")
    output.append("")
    return "\n".join(output)


def generate_category_section(category_key: str, category_info: dict, projects: list) -> str:
    output = []
    output.append(f"# {category_info['name']}")
    output.append("")
    output.append(category_info['description'])
    output.append("")
    for project in sorted(projects, key=lambda p: p['name']):
        output.append(generate_project_section(project))
    return "\n".join(output)


def generate_toc(categories: dict, projects_by_category: dict) -> str:
    output = []
    output.append("## Table of Contents")
    output.append("")
    output.append("<!-- INDEX_START -->")
    output.append("")
    for cat_key in sorted(categories.keys()):
        if cat_key == "unknown":
            continue
        cat_info = categories[cat_key]
        count = len(projects_by_category.get(cat_key, []))
        if count > 0:
            anchor = cat_info['name'].lower().replace(' ', '-').replace('&', '').replace('  ', '-')
            output.append(f"- [{cat_info['name']}](#{anchor})")
    output.append("")
    output.append("<!-- INDEX_END -->")
    output.append("")
    return "\n".join(output)


def generate_authors_section(projects: list) -> str:
    output = []
    output.append("# Authors")
    output.append("")
    output.append("Alphabetical list of contributors whose projects are listed here:")
    output.append("")
    authors = {}
    for project in projects:
        author = project.get('author')
        author_url = project.get('author_url')
        if author and author not in authors:
            authors[author] = author_url
    for author in sorted(authors.keys()):
        author_url = authors[author]
        if author_url:
            output.append(f"- [{author}]({author_url})")
        else:
            output.append(f"- {author}")
    output.append("")
    return "\n".join(output)


def generate_readme(projects_data: dict) -> str:
    output = []
    output.append("# AI Geopolitical Wargaming & Policy Simulation Projects")
    output.append("")
    output.append("A curated list of projects using AI, LLMs, and multi-agent systems for geopolitical wargaming, policy simulation, conflict modeling, and strategic forecasting.")
    output.append("")

    projects_by_category = defaultdict(list)
    for project in projects_data['projects']:
        projects_by_category[project['category']].append(project)

    output.append(f"*Last updated: {projects_data['metadata']['last_updated']}*")
    output.append("")

    output.append(generate_toc(projects_data['categories'], projects_by_category))

    for cat_key in sorted(projects_data['categories'].keys()):
        if cat_key == "unknown":
            continue
        projects = projects_by_category.get(cat_key, [])
        if len(projects) > 0:
            cat_info = projects_data['categories'][cat_key]
            output.append(generate_category_section(cat_key, cat_info, projects))

    if 'unknown' in projects_by_category and len(projects_by_category['unknown']) > 0:
        output.append("# Other Projects")
        output.append("")
        output.append("Projects that need categorization.")
        output.append("")
        for project in projects_by_category['unknown']:
            output.append(generate_project_section(project))

    if projects_data['projects']:
        output.append(generate_authors_section(projects_data['projects']))

    output.append("# Contributing")
    output.append("")
    output.append("Anyone is welcome to open a pull request to add a project to this list.")
    output.append("")
    output.append("To add a new project:")
    output.append("1. Fork this repository")
    output.append("2. Add your project to `projects.json` using the update script:")
    output.append("   ```bash")
    output.append("   ./update-projects.py --add https://github.com/username/repo --category category-name")
    output.append("   ```")
    output.append("3. Run the README generator:")
    output.append("   ```bash")
    output.append("   ./generate-readme.py")
    output.append("   ```")
    output.append("4. Submit a pull request")
    output.append("")
    output.append("Alternatively, drop me a line at public@danielrosehill.com if you'd like me to add it manually.")
    output.append("")

    output.append("# Disclaimer")
    output.append("")
    output.append("This resource is intended for those discovering AI-powered geopolitical simulation and wargaming projects. It is not exhaustive and is maintained on a best-effort basis.")
    output.append("")
    output.append("The inclusion of a project in this list does not constitute an endorsement. Users should evaluate each project independently for their specific use cases.")
    output.append("")

    output.append("---")
    output.append("")
    output.append(f"*Last updated: {projects_data['metadata']['last_updated']}*")
    output.append("")
    output.append("Maintained by [Daniel Rosehill](https://github.com/danielrosehill)")

    return "\n".join(output)


def main():
    projects_file = Path(__file__).parent / "projects.json"
    projects_data = load_projects_data(projects_file)
    readme_content = generate_readme(projects_data)
    readme_file = Path(__file__).parent / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Generated README.md")
    print(f"  Total projects: {projects_data['metadata']['total_projects']}")
    print(f"  Categories: {len(projects_data['categories'])}")


if __name__ == "__main__":
    main()
