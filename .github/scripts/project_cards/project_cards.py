import os
import requests

# GitHub token
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

def generate_project_svg(label_text, label_color, count):
    width = 140
    height = 120
    label_width = len(label_text) * 8 + 5

    # Create SVG content
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="black"/>
            </filter>
        </defs>

        <!-- Card Background with Shadow -->
        <rect x="5" y="5" width="{width-10}" height="{height-10}" rx="12" fill="#212830" filter="url(#shadow)"/>

        <!-- Label -->
        <g transform="translate({width/2}, 20)">
            <rect x="{-label_width/2}" y="0" width="{label_width}" height="24" rx="12" fill="{label_color}" fill-opacity="0.2" stroke="{label_color}" stroke-width="0.5"/>
            <text x="0" y="17" font-size="14" fill="{label_color}" font-family="Arial" text-anchor="middle">{label_text}</text>
        </g>

        <!-- Text -->
        <text x="{width/2}" y="90" font-size="40" fill="#9198a1" font-family="Arial" text-anchor="middle">{count}</text>
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
        discussions {{ totalCount }}
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
        "discussions": data["discussions"]["totalCount"]
    }


def generate_svgs():
    projects = [
        {"name": "Atta", "description": "TODO", "status": get_project_status("atta")},
        {"name": "ImPlot3D", "description": "TODO", "status": get_project_status("implot3d")},
        {"name": "Object Transportation Swarm", "description": "TODO", "status": get_project_status("object-transportation")},
        {"name": "CPU Simulator", "description": "TODO", "status": get_project_status("MyMachine")},
    ]
    print(projects)

generate_svgs()
