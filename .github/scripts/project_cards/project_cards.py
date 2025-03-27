import os
import requests

# GitHub token
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

STAR_PATH = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"
REPO_PATH = "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"
ISSUE_OPEN_PATH = "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"
ISSUE_CLOSED_PATH = "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0Zm-1.5 0a6.5 6.5 0 1 0-13 0 6.5 6.5 0 0 0 13 0ZM11.28 6.78a.75.75 0 0 0-1.06-1.06L7.25 8.69 5.78 7.22a.75.75 0 0 0-1.06 1.06l2 2a.75.75 0 0 0 1.06 0l3.5-3.5Z"
PR_OPEN_PATH = "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z"
PR_CLOSED_PATH = "M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z"
DISCUSSION_OPEN_PATH = "M1.75 1h8.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 10.25 10H7.061l-2.574 2.573A1.458 1.458 0 0 1 2 11.543V10h-.25A1.75 1.75 0 0 1 0 8.25v-5.5C0 1.784.784 1 1.75 1ZM1.5 2.75v5.5c0 .138.112.25.25.25h1a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h3.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm13 2a.25.25 0 0 0-.25-.25h-.5a.75.75 0 0 1 0-1.5h.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 14.25 12H14v1.543a1.458 1.458 0 0 1-2.487 1.03L9.22 12.28a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l2.22 2.22v-2.19a.75.75 0 0 1 .75-.75h1a.25.25 0 0 0 .25-.25Z"
DISCUSSION_CLOSED_PATH = "M0 2.75C0 1.783.784 1 1.75 1h8.5c.967 0 1.75.783 1.75 1.75v5.5A1.75 1.75 0 0 1 10.25 10H7.061l-2.574 2.573A1.457 1.457 0 0 1 2 11.543V10h-.25A1.75 1.75 0 0 1 0 8.25Zm1.75-.25a.25.25 0 0 0-.25.25v5.5c0 .138.112.25.25.25h1a.75.75 0 0 1 .75.75v2.189L6.22 8.72a.747.747 0 0 1 .53-.22h3.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25Zm12.5 2h-.5a.75.75 0 0 1 0-1.5h.5c.967 0 1.75.783 1.75 1.75v5.5A1.75 1.75 0 0 1 14.25 12H14v1.543a1.457 1.457 0 0 1-2.487 1.03L9.22 12.28a.749.749 0 1 1 1.06-1.06l2.22 2.219V11.25a.75.75 0 0 1 .75-.75h1a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25Zm-5.47.28-3 3a.747.747 0 0 1-1.06 0l-1.5-1.5a.749.749 0 1 1 1.06-1.06l.97.969L7.72 3.72a.749.749 0 1 1 1.06 1.06Z"

def generate_project_svg(project):
    width = 300
    height = 300
    font_size = 20

    # Mapping status keys to icon paths and CSS classes
    ICON_MAP = [
        ("stars", STAR_PATH, "default"),
        ("open_issues", ISSUE_OPEN_PATH, "open"),
        ("closed_issues", ISSUE_CLOSED_PATH, "closed"),
        ("open_prs", PR_OPEN_PATH, "open"),
        ("closed_prs", PR_CLOSED_PATH, "closed"),
        ("open_discussions", DISCUSSION_OPEN_PATH, "open"),
        ("closed_discussions", DISCUSSION_CLOSED_PATH, "closed"),
    ]

    # Build footer
    footer = ""
    footer_x = 10
    for key, path, icon_class in ICON_MAP:
        count = project.get("status", {}).get(key, 0)
        if count > 0:
            footer += f"""
            <g transform="translate({footer_x}, {height - 15})">
                <path class="icon {icon_class}" transform="translate(0, -13)" d="{path}"/>
                <text x="19" y="0" text-anchor="start">{count}</text>
            </g>
            """
            digit_width = 7  # Rough estimate per digit in Arial 12px
            text_width = digit_width * len(str(count))
            footer_x += 19 + text_width + 10  # Icon offset + text + spacing

    # Create SVG content
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <style>
            :root {{
                 --border-color: #D1D9E0;
                 --icon-open: #1a7f37;
                 --icon-closed: #8250df;
                 --icon-default: #59636e;
                 --title-color: #0969da;
                 --text-color: #59636e;
             }}

            text {{
                font-family: Arial, sans-serif;
                font-size: 12px;
                fill: var(--text-color);
            }}

            text.title {{
                fill: var(--title-color);
                font-size: 14px;
                font-weight: bold;
            }}

             rect.card {{
                 fill: none;
                 stroke: var(--border-color);
                 stroke-width: 2px;
                 rx: 6px;
                 ry: 6px;
             }}

             .icon.open {{
                 fill: var(--icon-open);
             }}

             .icon.closed {{
                 fill: var(--icon-closed);
             }}

             .icon.default {{
                 fill: var(--icon-default);
             }}

             .title {{
                 fill: var(--title-color);
             }}

             .description {{
                 fill: var(--text-color);
             }}

             @media (prefers-color-scheme: dark) {{
                 :root {{
                     --border-color: #3D444D;
                     --icon-open: #57ab5a;
                     --icon-closed: #986ee2;
                     --icon-default: #9198a1;
                     --title-color: #478be6;
                     --text-color: #9198a1;
                 }}
             }}
        </style>

        <!-- Card Border -->
        <rect class="card" x="0" y="0" width="{width}" height="{height}"/>

        <!-- Icon + Project Name -->
        <g transform="translate(15, 15)">
            <path class="icon default" d="{REPO_PATH}"/>
            <text class="title" x="20" y="12">{project["name"]}</text>
        </g>

        <!-- Footer -->
        {footer}
    </svg>
    """

    return svg

def get_project_status(repo):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    query = f"""
    {{
      repository(owner: "brenocq", name: "{repo}") {{
        stargazerCount
        issues(states: OPEN) {{ totalCount }}
        closed_issues: issues(states: CLOSED) {{ totalCount }}
        open_prs: pullRequests(states: OPEN) {{ totalCount }}
        all_prs: pullRequests {{ totalCount }}
        open_dis: discussions(states: OPEN) {{ totalCount }}
        closed_dis: discussions(states: CLOSED) {{ totalCount }}
      }}
    }}
    """

    response = requests.post(url, headers=headers, json={"query": query})
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    data = response.json()["data"]["repository"]

    return {
        "stars": data["stargazerCount"],
        "open_issues": data["issues"]["totalCount"],
        "closed_issues": data["closed_issues"]["totalCount"],
        "open_prs": data["open_prs"]["totalCount"],
        "closed_prs": data["all_prs"]["totalCount"] - data["open_prs"]["totalCount"],
        "open_discussions": data["open_dis"]["totalCount"],
        "closed_discussions": data["closed_dis"]["totalCount"]
    }
    #return {
    #    "stars": 867,
    #    "open_issues": 0,
    #    "closed_issues": 2,
    #    "open_prs": 1,
    #    "closed_prs": 30,
    #    "open_discussions": 33,
    #    "closed_discussions": 2,
    #}


def generate_svgs():
    projects = [
        {"name": "Atta", "description": "TODO", "status": get_project_status("atta")},
        {"name": "ImPlot3D", "description": "TODO", "status": get_project_status("implot3d")},
        {"name": "Object Transportation Swarm", "description": "TODO", "status": get_project_status("object-transportation")},
        {"name": "CPU Simulator", "description": "TODO", "status": get_project_status("MyMachine")},
    ]
    for project in projects:
        filename = f"{project['name'].replace(' ', '_').lower()}.svg"
        print(f'Generating {filename} from project {projects}')
        svg = generate_project_svg(project)
        with open(filename, "w") as f:
            f.write(svg)

generate_svgs()
