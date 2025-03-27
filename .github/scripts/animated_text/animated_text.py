TEXT = "Hi there! I'm Bruno|<<<endon|<<<no|<<o"
FILENAME = "brenocq_typing.svg"

def build_svg_animation(text: str) -> str:
    width = 210
    height = 30
    font_size = 20

    # Build <text> blocks for each step of the typing
    lines = []
    visible = ""
    step = 0
    time = 0
    for idx, char in enumerate(text):
        if char == "|":
            continue
        if char == "<":
            visible = visible[:-1]  # backspace
        else:
            visible += char

        # Make sure to freeze the last step
        is_last_step = (idx == len(text) - 1)
        fill_type = "freeze" if is_last_step else "remove"

        # Compute delay between chars
        is_pause = text[idx + 1] == "|" if not is_last_step else False
        delay = 1.0 if is_pause else 0.15

        lines.append(f"""
        <text x="0" y="{font_size}" text-anchor="start" opacity="0">
            <set attributeName="opacity" to="1" begin="{round(time, 3)}s" dur="{delay}" fill="{fill_type}" />
            {visible}
        </text>
        """)
        step += 1
        time += delay

    emoji_x = len(visible) * font_size * 0.48;
    pivot_x = emoji_x + 22
    pivot_y = font_size

    # Create SVG content
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <!-- Made as a joke by brenocq, people get my name wrong all the same at Starbucks -->
        <style>
            text {{
                font-family: Arial, sans-serif;
                font-weight: bold;
                font-size: {font_size}px;
                fill: #1F2328;
                opacity: 0;
            }}
            @media (prefers-color-scheme: dark) {{
                text {{
                    fill: #D1D7E0;
                }}
            }}
        </style>

        <!-- Typing text -->
        {''.join(lines)}

        <!-- Animated emoji -->
        <text x="{emoji_x}" y="{font_size}" text-anchor="start" opacity="0">
            <set attributeName="opacity" to="1" begin="{round(time+2*delay, 3)}s" dur="0.001s" fill="freeze" />
            👋
            <animateTransform attributeName="transform"
                type="rotate"
                values="-20 {pivot_x} {pivot_y}; 20 {pivot_x} {pivot_y}; -20 {pivot_x} {pivot_y}"
                dur="0.5s"
                repeatCount="indefinite" />
        </text>
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
