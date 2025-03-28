import requests
import base64
from io import BytesIO
from PIL import Image

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


def generate_svg() -> str:
    width = 800
    height = 50

    # Mikinho
    mikinho = ""
    mike_x = 700
    try:
        encoded_image, img_width, img_height = encode_image_base64("https://brenocq.s3.us-east-1.amazonaws.com/readme-mike.png")

        target_height = 50
        aspect_ratio = img_width / img_height
        target_width = int(target_height * aspect_ratio)

        mikinho = f"""
        <image
          href="{encoded_image}"
          x="{0}"
          y="{50}"
          height="{target_height}"
          width="{target_width}">
            <!-- Vertical spooky Mike -->
            <animate attributeName="y"
              values="50;0;0;50;50"
              keyTimes="0;0.01;0.26;0.86;1"
              begin="2s"
              dur="9s"
              repeatCount="indefinite"
              fill="freeze"
              calcMode="spline"
              keySplines="0.4 0 0.2 1; 0 0 1 1; 0.4 0 0.2 1; 0 0 1 1"/>

            <!-- Horizontal movement cycle (one per bounce) -->
            <animate attributeName="x"
              values="30;{width - target_width - 30};{width // 2 - target_width // 2};30"
              keyTimes="0;0.33;0.66;1"
              begin="0s"
              dur="27s"
              repeatCount="indefinite"
              fill="freeze"
              calcMode="discrete" />
        </image>
        """
    except Exception as e:
        print(f"Warning: could not load image: {e}")

    # Build SVG
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
        <style>
            :root {{
                --border-color: #d1d9e0;
            }}
            @media (prefers-color-scheme: dark) {{
                :root {{
                    --border-color: #3d444d;
                }}
            }}

            rect.divider {{
                fill: var(--border-color);
            }}
        </style>

        <!-- Divider -->
        <rect class="divider" x="0" y="{height-1}" width="{width}" height="1" />

        <!-- Mikinho -->
        {mikinho}
    </svg>
    """

def save_svg(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)
    print(f"Saved SVG to {filename}")

if __name__ == "__main__":
    svg = generate_svg()
    save_svg(f"divider.svg", svg)
