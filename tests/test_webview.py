import pytest
from playwright.sync_api import sync_playwright, expect
import json
import urllib.parse
import http.server
import threading

# --- Server Fixture ---

class SimpleHTTPServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging
        return

@pytest.fixture(scope="session")
def server():
    # Serve from root so assets/webview.html is accessible
    port = 8000
    handler = SimpleHTTPServer
    httpd = http.server.HTTPServer(("127.0.0.1", port), handler)

    # Run server in a thread
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://127.0.0.1:{port}"

    httpd.shutdown()
    httpd.server_close()

# --- Playwright Fixtures ---

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "args": [
            "--use-fake-ui-for-media-stream",
            "--use-fake-device-for-media-stream",
        ]
    }

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance, browser_context_args):
    # Launch with media stream flags
    browser = playwright_instance.chromium.launch(
        headless=True,
        args=browser_context_args["args"]
    )
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

# --- Tests ---

def test_camera_mode(page, server):
    page.goto(f"{server}/assets/webview.html?mode=camera")
    # Verify key elements exist
    expect(page.locator("#cam-video")).to_be_attached()
    expect(page.locator("#cam-mic")).to_be_visible()
    expect(page.locator("#cam-status")).to_be_visible()

def test_record_mode(page, server):
    page.goto(f"{server}/assets/webview.html?mode=record")
    expect(page.locator("#mic-btn")).to_be_visible()
    expect(page.locator("#rec-status")).to_be_visible()
    expect(page.locator(".hdr-title")).to_contain_text("实时气泡字幕")

def test_play_mode(page, server):
    data = {
        "segments": [
            {"start": 0, "end": 2, "text": "Hello world", "speaker": "A", "position": "center"}
        ],
        "duration": 5,
        "title": "Test Title"
    }
    encoded_data = urllib.parse.quote(json.dumps(data))
    page.goto(f"{server}/assets/webview.html?mode=play&data={encoded_data}")

    expect(page.locator("#btn-play")).to_be_visible()
    expect(page.locator("#prog-track")).to_be_visible()
    expect(page.locator(".hdr-title")).to_have_text("Test Title")
