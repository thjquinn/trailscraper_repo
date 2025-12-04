from playwright.sync_api import sync_playwright, TimeoutError

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.hikingproject.com/directory/8010491/utah")

# Click first button
if page.get_by_text("Show More Trails", exact=True).is_visible():
    page.get_by_text("Show More Trails", exact=True).click()
    page.wait_for_timeout(800)
    page.mouse.wheel(0, 50000)

# Click "Show More" repeatedly
while True:
    btn = page.get_by_text("Show More", exact=True)
    if not btn.is_visible():
        break

    btn.click()

    try:
        page.wait_for_timeout(800)  # allow new trails to load
    except TimeoutError:
        break

    page.mouse.wheel(0, 50000)  # reveal next button

links = page.eval_on_selector_all(
        "a[href*='/trail/']",
        "els => els.map(e => e.href)"
    )

print(links)

import csv

with open("utah_links.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["link"])  # header
    for item in links:
        writer.writerow([item])


page.close()

browser.close()

pw.stop()
