import os
import requests
import base64
from io import BytesIO
from PIL import Image
import boto3

# AWS
s3 = boto3.client("s3")

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

def build_char_width_table(default=6):
    """Build an estimated width table for ASCII chars."""
    table = {}
    for chars, width in [
        ("iIl.", 3),
        ("fjrt", 4),
        ("abcdeghknopqsuvxyz", 6),
        ("mw", 8),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 8),
        ("0123456789", 6),
        ("-_=+[](){} ", 5),
        ("!\"#$%&'*<>?,;:/\\|`~", 4),
    ]:
        for c in chars:
            table[c] = width
    return table

CHAR_WIDTH_TABLE = build_char_width_table()

def estimate_word_width(word):
    return sum(CHAR_WIDTH_TABLE.get(c, 6) for c in word)

def wrap_text(text, max_width):
    """Wrap text based on estimated pixel width."""
    words = text.split()
    lines = []
    current_line = ""
    current_width = 0

    for word in words:
        word_width = estimate_word_width(word)
        space_width = CHAR_WIDTH_TABLE.get(" ", 3)
        if current_line:
            word_width += space_width

        if current_width + word_width <= max_width:
            current_line += (" " if current_line else "") + word
            current_width += word_width
        else:
            lines.append(current_line)
            current_line = word
            current_width = estimate_word_width(word)

    if current_line:
        lines.append(current_line)

    return lines

def encode_image_base64(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download image from {image_url}")

    content_type = response.headers.get("Content-Type")
    if content_type is None or not content_type.startswith("image/"):
        raise Exception(f"Invalid Content-Type: {content_type}")

    # Get image dimensions
    img = Image.open(BytesIO(response.content))
    img_width, img_height = img.size

    # Base64 encode
    encoded = base64.b64encode(response.content).decode("utf-8")
    data_uri = f"data:{content_type};base64,{encoded}"

    return data_uri, img_width, img_height

def generate_project_svg(project):
    width = 350
    height = 300
    padding = 15

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

    # Image block
    image_x = 0
    image_y = padding + 25
    target_width = 0
    target_height = 0
    fade_image_delay = 0.1
    image = ""
    if "image" in project and project["image"]:
        try:
            encoded_image, img_width, img_height = encode_image_base64(project["image"])

            target_height = 130
            aspect_ratio = img_width / img_height
            target_width = int(target_height * aspect_ratio)
            image_x = (width - target_width) // 2

            image = f"""
            <g opacity="0">
                <animate attributeName="opacity" from="0" to="1" begin="{fade_image_delay}s" dur="0.4s" fill="freeze"/>
                <image
                  href="{encoded_image}"
                  x="{image_x}"
                  y="{image_y}"
                  height="{target_height}"
                  width="{target_width}"
                  clip-path="url(#rounded-image)" />
            </g>
            """
        except Exception as e:
            print(f"Warning: could not load image: {e}")

    # Wrapped description block
    description_text = project.get("description", "No description provided.")
    fade_description_delay = fade_image_delay + 0.2  # small gap after image
    description_y = image_y + target_height + padding + 5
    description_lines = wrap_text(description_text, max_width=width - 2 * padding)

    description_inner = ""
    for i, line in enumerate(description_lines):
        dy = "0" if i == 0 else "1.2em"
        description_inner += f'  <tspan x="{padding}" dy="{dy}">{line}</tspan>\n'

    description = f"""
    <g opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{fade_description_delay}s" dur="0.4s" fill="freeze"/>
        <text class="description" x="{padding}" y="{description_y}">
            {description_inner.strip()}
        </text>
    </g>
    """

    footer = ""
    footer_x = padding
    animation_index = 0
    for key, path, icon_class in ICON_MAP:
        count = project.get("status", {}).get(key, 0)
        if count > 0:
            delay = round(animation_index * 0.2, 2)
            footer += f"""
            <g transform="translate({footer_x}, {height - padding})" opacity="0">
                <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>
                <path class="icon {icon_class}" transform="translate(0, -13)" d="{path}"/>
                <text x="19" y="0" text-anchor="start">{count}</text>
            </g>
            """
            digit_width = 7  # Rough estimate per digit
            text_width = digit_width * len(str(count))
            footer_x += 19 + text_width + 10
            animation_index += 1

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

        <!-- Rounded Image -->
        <defs>
          <clipPath id="rounded-image">
            <rect x="{image_x}" y="{image_y}" width="{target_width}" height="{target_height}" rx="6" ry="6"/>
          </clipPath>
        </defs>

        <!-- Card Border -->
        <rect class="card" x="0" y="0" width="{width}" height="{height}"/>

        <!-- Icon + Project Name -->
        <g transform="translate({padding}, {padding})">
            <path class="icon default" d="{REPO_PATH}"/>
            <text class="title" x="20" y="12">{project["name"]}</text>
        </g>

        <!-- Image -->
        {image}

        <!-- Description -->
        {description}

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


def generate_svgs():
    projects = [
        {"name": "Atta", "description": "A robot simulator built from scratch, supporting multi-sensor simulation (IR, camera, touch), physics (Box2D, Bullet), OpenGL/Vulkan rendering, cross-platform compatibility (Windows, macOS, Linux, Web), and extensible C++ scripting.", "status": get_project_status("atta"), "image": "https://brenocq.s3.us-east-1.amazonaws.com/readme-atta.png"},
        {"name": "ImPlot3D", "description": "ImPlot3D extends Dear ImGui by offering accessible, high-performance 3D plotting capabilities. Drawing inspiration from ImPlot, it offers a user-friendly API for developers familiar with ImPlot. ImPlot3D is specifically crafted for generating 3D plots featuring customizable markers, lines, surfaces, images, and meshes.", "status": get_project_status("implot3d"), "image": "https://brenocq.s3.us-east-1.amazonaws.com/readme-implot3d.jpg"},
        {"name": "Object Transportation Swarm", "description": "This project extends Chen (2015) by enabling a swarm of miniature vision-based robots to transport objects around obstacles using sub-goal formation. The approach remains decentralized, communication-free, and vision-driven, allowing efficient object transport in complex environments.", "status": get_project_status("object-transportation"), "image": "https://brenocq.s3.us-east-1.amazonaws.com/readme-object-transportation.png"},
        {"name": "CPU Simulator", "description": "I designed a custom assembly language along with an assembler to convert the assembly code into binary. Additionally, I developed a CPU simulator capable of executing the binary instructions, with the output displayed on a curses-based screen. To demonstrate the system, I created two games specifically for this CPU.", "status": get_project_status("MyMachine"), "image": "https://brenocq.s3.us-east-1.amazonaws.com/readme-cpu-simulator.png"},
    ]
    for project in projects:
        filename = f"readme-{project['name'].replace(' ', '-').lower()}.svg"
        print(f'Generating {filename} from project {projects}')
        svg = generate_project_svg(project)
        with open(filename, "w") as f:
            f.write(svg)
        print(f'Uploaded {filename} to S3')
        s3.upload_file(filename, "brenocq", filename, ExtraArgs={"ContentType": "image/svg+xml"})

generate_svgs()
