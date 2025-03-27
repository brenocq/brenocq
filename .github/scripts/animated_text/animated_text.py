TEXT = "Hi there! I'm Breno 👋"
FILENAME = "brenocq_typing.svg"

def build_svg_animation(text: str) -> str:
    width = 210
    height = 30
    font_size = 20

    # Create SVG content
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <style>
            text {{
                font-family: Arial, sans-serif;
                font-weight: bold;
                font-size: {font_size}px;
                fill: #1F2328;
            }}
            @media (prefers-color-scheme: dark) {{
                text {{
                    fill: #D1D7E0;
                }}
            }}
        </style>
        <text x="0" y="{font_size}" text-anchor="start">{text}</text>
    </svg>
    """
    return svg

def save_svg(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)
    print(f"Saved SVG to {filename}")

if __name__ == "__main__":
    svg_content = build_svg_animation(TEXT)
    save_svg(FILENAME, svg_content)
