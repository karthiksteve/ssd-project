"""
Captures high-resolution pixel-perfect demo screenshots of RescuePath AI
across all operational tabs and basins using Playwright.
"""

import os
import time
from playwright.sync_api import sync_playwright

ASSETS_DIR = r"c:\Users\speak\Downloads\ssd_project\docs_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def capture_all():
    print("Starting Playwright demo screen capture...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # 1. Main Evacuation Routing View (Kerala)
        print("Navigating to http://localhost:5173 ...")
        page.goto("http://localhost:5173", wait_until="networkidle")
        time.sleep(3) # allow Leaflet tiles to load
        
        path1 = os.path.join(ASSETS_DIR, "demo_01_evacuation_routing.png")
        page.screenshot(path=path1)
        print(f"Captured: {path1}")

        # 2. Sequential Timeline Panel (Forecast tab)
        print("Switching to Forecast tab...")
        page.locator('.sidebar-tabs button:has-text("Forecast")').click()
        time.sleep(2)
        path2 = os.path.join(ASSETS_DIR, "demo_02_sequential_timeline.png")
        page.screenshot(path=path2)
        print(f"Captured: {path2}")

        # 3. Spatial Clusters & Moran's I Panel (Clusters tab)
        print("Switching to Clusters tab...")
        page.locator('.sidebar-tabs button:has-text("Clusters")').click()
        time.sleep(2)
        path3 = os.path.join(ASSETS_DIR, "demo_03_spatial_clusters.png")
        page.screenshot(path=path3)
        print(f"Captured: {path3}")

        # 4. Shelter Directory Panel (Shelters tab)
        print("Switching to Shelters tab...")
        page.locator('.sidebar-tabs button:has-text("Shelters")').click()
        time.sleep(2)
        path4 = os.path.join(ASSETS_DIR, "demo_04_shelter_directory.png")
        page.screenshot(path=path4)
        print(f"Captured: {path4}")

        # 5. Disaster Surge Simulation Panel (Crisis tab)
        print("Switching to Crisis simulation tab...")
        page.locator('.sidebar-tabs button:has-text("Crisis")').click()
        time.sleep(2)
        path5 = os.path.join(ASSETS_DIR, "demo_05_surge_simulation.png")
        page.screenshot(path=path5)
        print(f"Captured: {path5}")

        # 6. Assam Guwahati Basin Switch
        print("Switching region to Assam Guwahati...")
        page.locator('select.select-custom').first.select_option("assam_guwahati")
        time.sleep(4) # Wait for network requests and map tile animation
        
        # Switch back to Routing tab
        page.locator('.sidebar-tabs button:has-text("Routing")').click()
        time.sleep(3)
        path6 = os.path.join(ASSETS_DIR, "demo_06_assam_guwahati.png")
        page.screenshot(path=path6)
        print(f"Captured: {path6}")

        browser.close()
        print("All 6 demo screenshots captured successfully!")

if __name__ == "__main__":
    capture_all()
