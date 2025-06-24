
from playwright.sync_api import Playwright, sync_playwright, Page, Locator
import os
import subprocess
from datetime import datetime
import time


def convert_webm_to_mp4(input_path: str, output_dir: str | None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found.")

    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"playwright_recording_{timestamp}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    command = [
        "ffmpeg",
        "-i", input_path,
        "-ss", "1",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-y",
        output_path,
        "-vf", "scale=432:936:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"
    ]

    subprocess.run(command, check=True)
    return output_path


def add_title(page: Page, title: str, mainTitle: bool = False) -> None:
    """Add a title to the page."""
    page.evaluate(
        """
        ({ title, mainTitle }) => {
            const titleDiv = document.createElement("div");
            titleDiv.className = "bottom-title show-title";
            if (mainTitle) {
                titleDiv.style.backgroundColor = "rgb(234, 88, 12)";
            }
            titleDiv.innerText = title;
            document.body.appendChild(titleDiv);
            setTimeout(() => titleDiv.classList.remove("show-title"), 2000);
        }
        """,
        {"title": title, "mainTitle": mainTitle}
    )
    page.wait_for_timeout(2500)  # Wait for the title to be displayed


def create_ripple(page: Page, locator: Locator) -> None:
    page.evaluate(
        """
    (el) => {
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const x = rect.left + rect.width / 2 + window.scrollX;
        const y = rect.top + rect.height / 2 + window.scrollY;

        const ripple = document.createElement("div");
        ripple.className = "ripple-circle";
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        document.body.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }
    """,
        locator.element_handle()
    )


def click_with_ripple(page: Page, locator: Locator, delay: float = 500, double_click: bool = False) -> None:
    create_ripple(page, locator)

    # Trigger second ripple for double click
    if double_click:
        time.sleep(0.2)
        create_ripple(page, locator)

    # Delay before click
    time.sleep(delay / 1000)

    # Perform the click
    if double_click:
        locator.dblclick()
    else:
        locator.click()


def run(playwright: Playwright) -> None:
    device = playwright.devices["iPhone 14 Pro Max"]
    browser = playwright.chromium.launch(headless=True, slow_mo=2000, args=[
        "--high-dpi-support=1",
        f"--force-device-scale-factor={device['device_scale_factor']}",
    ])
    context = browser.new_context(
        **device,
        record_video_dir="./clips",
        record_video_size={
            "width": device["viewport"]["width"] * device["device_scale_factor"],
            "height": device["viewport"]["height"] * device["device_scale_factor"]
        },
        locale="ar",

    )
    page = context.new_page()
    # print(css_content)
    page.goto("https://app.turath.io")
    page.add_style_tag(path='../clip.css')

    # Wait for the page to load
    page.wait_for_load_state("networkidle")

    ''' add your code here  '''

    # ---------------------
    context.close()
    browser.close()

    # After closing, get the video path from the first video in the context
    video_path = page.video.path() if page.video else None
    mp4_path = convert_webm_to_mp4(str(video_path), None)
    print(f"Converted video saved at: {mp4_path}")
    if video_path is not None:
        os.remove(video_path)


with sync_playwright() as playwright:
    run(playwright)
