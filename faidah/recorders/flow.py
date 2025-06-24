import time
from datetime import datetime
import subprocess
import os
from playwright.sync_api import Playwright, sync_playwright, Page, Locator


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
        "-ss", "1.5",
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
                titleDiv.style.backgroundColor = "#174DE2";
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
    browser = playwright.chromium.launch(headless=True, slow_mo=1200, args=[
        "--high-dpi-support=1",
        f"--force-device-scale-factor={device['device_scale_factor']}",
    ])
    context = browser.new_context(
        **device,
        record_video_dir="./clips/",
        record_video_size={
            "width": device["viewport"]["width"] * device["device_scale_factor"],
            "height": device["viewport"]["height"] * device["device_scale_factor"]
        },
        locale="ar",

    )
    page = context.new_page()
    # print(css_content)
    page.goto("https://app.faidah.app/")
    page.add_style_tag(path='../clip.css')

    # Wait for the page to load
    page.wait_for_load_state("networkidle")
    add_title(page, "تطبيق فائدة", mainTitle=True)
    click_with_ripple(page, page.get_by_role("button", name="التالي"))

    add_title(page, "يمكنك اختيار المواد من القائمة المقترحة")
    click_with_ripple(page, page.get_by_role(
        "button", name="رياض الصالحين ت الفحل الكتاب: رياض الصالحين المؤلف: أبو زكريا محيي الدين يحيى بن"))
    page.get_by_role("listitem").nth(1).click()
    click_with_ripple(page, page.get_by_role(
        "button", name="أول مرة أتدبر القرآن الكتاب: أول مرة أتدبر القرآن جمع وإعداد: عادل محمد خليل قدم"))
    page.get_by_role("listitem").nth(3).click()
    click_with_ripple(page, page.get_by_role(
        "button", name="خُلاصَةُ تَعْظِيمِ العِلمِ من تأليف الشيخ صالح العصيمي، لخصه من كتابه «تعظيم الع"))
    click_with_ripple(page, page.get_by_role("button", name="اشتراك"))
    page.wait_for_load_state("networkidle")

    add_title(page, "قراءة المواد")
    click_with_ripple(page, page.get_by_role(
        "link", name="رياض الصالحين ت الفحل الكتاب: رياض الصالحين المؤلف: أبو زكريا محيي الدين يحيى بن"))
    page.locator("#pg-10").hover()
    page.mouse.wheel(0, 500)
    page.locator("#pg-11").hover()
    page.mouse.wheel(0, 800)

    add_title(page, "إضافة علامة أينما توقفت")
    click_with_ripple(page, page.locator(
        "#pg-12").get_by_role("button", name="علم كمقروء"))
    page.wait_for_timeout(2500)
    # add_title(page, "البحث عن المواد في المكتبة")
    # click_with_ripple(page, page.get_by_role("link", name="مكتبة"))
    # click_with_ripple(page, page.get_by_role("textbox", name="بحث"))
    # page.get_by_role("textbox", name="بحث").fill("مختصر السيرة")
    # click_with_ripple(page, page.get_by_role(
    #     "button", name="المختصر في السيرة النبوية (اكتملت السلسلة) عام الرسائل: ١٨٢"))

    # add_title(page, "جدولة المادة")
    # click_with_ripple(page, page.get_by_role("button", name="اشتراك مخصص"))
    # click_with_ripple(page, page.get_by_role("button", name="الأسبوع"))
    # click_with_ripple(page, page.locator(
    #     "label").filter(has_text="السبت").locator("div"))
    # click_with_ripple(page, page.locator("label").filter(
    #     has_text="الاثنين").get_by_role("img"))
    # click_with_ripple(page, page.locator("label").filter(
    #     has_text="الأربعاء").get_by_role("img"))
    # click_with_ripple(page, page.locator("label").filter(
    #     has_text="الجمعة").locator("div"))
    # click_with_ripple(page, page.get_by_role("textbox", name="وقت الإشعار"))
    # page.get_by_role("textbox", name="وقت الإشعار").fill("04:00")
    # page.get_by_role("textbox", name="وقت الإشعار").hover()
    # page.mouse.wheel(0, 50)
    # click_with_ripple(page, page.locator(
    #     "#vaul-svelte-2").get_by_role("button", name="اشتراك"))

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
