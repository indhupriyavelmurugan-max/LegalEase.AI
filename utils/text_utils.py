import html
import re


def sanitize_text(text: str) -> str:

    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-"
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    text = text.replace("\x00", "")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def format_html_preview(text: str) -> str:

    safe_text = html.escape(
        sanitize_text(text)
    )

    blocks = []

    for paragraph in safe_text.split("\n\n"):

        lines = paragraph.splitlines()

        non_empty = [
            line for line in lines
            if line.strip()
        ]

        if (
            non_empty
            and all(
                line.strip().startswith("- ")
                for line in non_empty
            )
        ):

            items = "".join(
                f"<li>{line.strip()[2:]}</li>"
                for line in non_empty
            )

            blocks.append(
                f"<ul>{items}</ul>"
            )

        else:

            blocks.append(
                f"<p>{'<br>'.join(lines)}</p>"
            )

    return "".join(blocks)