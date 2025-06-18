import re
from playwright.sync_api import Page, expect

def test_homepage_has_correct_title(page: Page):
    """Test that the homepage has the correct title."""
    # Note: The Flask app must be running for this test to pass.
    page.goto("http://127.0.0.1:5000/")
    
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("주역 8괘-64괘 수학적 매핑"))

def test_pi_verification_flow(page: Page):
    """Test the full user flow for Pi verification."""
    # Note: The Flask app must be running for this test to pass.
    # Navigate directly to the verification page
    page.goto("http://127.0.0.1:5000/verification")

    # Check if the URL is correct
    expect(page).to_have_url("http://127.0.0.1:5000/verification")

    # 1. Click the "π 원주율" tab to make the content visible
    page.get_by_role("button", name="π 원주율").click()

    # 2. Now click the "π 검증 시작" button inside the tab panel
    page.get_by_role("button", name="π 검증 시작").click()

    # Wait for the result container to have content and check for the image
    result_container_selector = "#piResults"
    result_container = page.locator(result_container_selector)
    
    # Wait for the container to be visible and have an image
    expect(result_container).to_be_visible(timeout=10000)

    # Check that the image inside the container is loaded
    image = result_container.locator("img")
    expect(image).to_have_attribute("src", re.compile(r"^data:image/png;base64,iVBORw0KGgo"))
