import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import get_chrome_driver
from hash_mal import hash_groups

def wait_for_element_to_exist(driver, css_selector, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(f"return document.querySelector('{css_selector}') !== null")
        )
        return True
    except TimeoutException:
        return False

def wait_for_shadow_element(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("""
                const shell = document.querySelector('vt-ui-shell');
                if (!shell) return false;
                const fileView = shell.querySelector('file-view');  // Direct child, not in shadowRoot
                if (!fileView || !fileView.shadowRoot) return false;
                const report = fileView.shadowRoot.querySelector('vt-ui-main-generic-report');
                return report !== null;
            """)
        )
        return True
    except TimeoutException:
        return False

def debug_shadow_structure(driver):
    result = driver.execute_script("""
        try {
            const shell = document.querySelector('vt-ui-shell');
            if (!shell) return {error: 'vt-ui-shell not found'};
            
            const fileView = shell.querySelector('file-view');  // Direct child, not in shadowRoot
            if (!fileView) return {error: 'file-view not found as direct child of vt-ui-shell'};
            if (!fileView.shadowRoot) return {error: 'file-view has no shadowRoot'};
            
            const report = fileView.shadowRoot.querySelector('vt-ui-main-generic-report');
            if (!report) return {error: 'vt-ui-main-generic-report not found'};
            if (!report.shadowRoot) return {error: 'vt-ui-main-generic-report has no shadowRoot'};
            
            const navTabs = report.shadowRoot.querySelector('.nav.nav-tabs.flex-nowrap');
            if (!navTabs) return {error: 'nav-tabs not found'};
            
            const navItems = navTabs.querySelectorAll('.nav-item');
            const tabTexts = Array.from(navItems).map((item, index) => ({
                index: index,
                text: item.textContent.trim(),
                hasATag: !!item.querySelector('a')
            }));
            
            return {
                success: true,
                navItemsCount: navItems.length,
                tabTexts: tabTexts
            };
        } catch (error) {
            return {error: error.message};
        }
    """)
    
    print(f"🔍 Shadow DOM Debug: {result}")
    return result

def click_behavior_tab(driver):
    try:
        print("⏳ Waiting for page to fully load...")
        time.sleep(10)
        
        debug_result = debug_shadow_structure(driver)
        if not debug_result.get('success'):
            print(f"❌ Shadow DOM structure issue: {debug_result.get('error')}")
            
            print("🔄 Trying alternative approach...")
            current_url = driver.current_url
            if '/behavior' not in current_url:
                behavior_url = current_url.replace('/detection', '/behavior') if '/detection' in current_url else current_url + '/behavior'
                print(f"📍 Navigating to: {behavior_url}")
                driver.get(behavior_url)
                time.sleep(8)
                
                debug_result = debug_shadow_structure(driver)
                if not debug_result.get('success'):
                    return False
        
        if debug_result.get('success'):
            nav_items = debug_result.get('tabTexts', [])
            print(f"📋 Found {len(nav_items)} navigation tabs:")
            for item in nav_items:
                print(f"  Tab {item['index']}: '{item['text']}' (has <a>: {item['hasATag']})")
            
            behavior_index = None
            for item in nav_items:
                if 'behavior' in item['text'].lower() or 'behaviour' in item['text'].lower():
                    behavior_index = item['index']
                    break
            
            if behavior_index is None and len(nav_items) > 6:
                behavior_index = 6
                print("🎯 Using index 6 as behavior tab")
            
            if behavior_index is not None:
                clicked = driver.execute_script(f"""
                    try {{
                        const shell = document.querySelector('vt-ui-shell');
                        const fileView = shell.querySelector('file-view');  // Direct child
                        const report = fileView.shadowRoot.querySelector('vt-ui-main-generic-report');
                        const navTabs = report.shadowRoot.querySelector('.nav.nav-tabs.flex-nowrap');
                        const navItems = navTabs.querySelectorAll('.nav-item');
                        
                        if (navItems.length > {behavior_index}) {{
                            const behaviorItem = navItems[{behavior_index}];
                            const link = behaviorItem.querySelector('a');
                            if (link) {{
                                link.click();
                                return true;
                            }}
                        }}
                        return false;
                    }} catch (error) {{
                        console.error('Click error:', error);
                        return false;
                    }}
                """)
                
                if clicked:
                    print(f"✅ Successfully clicked behavior tab at index {behavior_index}")
                    time.sleep(5)  
                    return True
                else:
                    print(f"❌ Failed to click behavior tab at index {behavior_index}")
            else:
                print("❌ Could not identify behavior tab")
        
        return False
        
    except Exception as e:
        print(f"❌ Error in click_behavior_tab: {e}")
        return False

def get_behavior_data(driver):
    try:
        if not click_behavior_tab(driver):
            print("Could not access behavior tab")
            return None
        
        time.sleep(5)
        
        behavior_loaded = driver.execute_script("""
            try {
                const shell = document.querySelector('vt-ui-shell');
                const fileView = shell.querySelector('file-view');  // Direct child
                const report = fileView.shadowRoot.querySelector('vt-ui-main-generic-report');
                const behaviors = report.querySelector('vt-ui-file-behaviours');
                return behaviors !== null;
            } catch (error) {
                return false;
            }
        """)
        
        if not behavior_loaded:
            print("Behavior content not loaded")
            return None
        
        behavior_data = driver.execute_script("""
            try {
                const shell = document.querySelector('vt-ui-shell');
                const fileView = shell.querySelector('file-view');  // Direct child
                const report = fileView.shadowRoot.querySelector('vt-ui-main-generic-report');
                const behaviors = report.querySelector('vt-ui-file-behaviours');
                
                if (!behaviors) {
                    return null;

                }
                
                const behavior = behaviors.shadowRoot.querySelector('vt-ui-behaviour');
                if (!behavior || !behavior.shadowRoot) {
                    return null;
                }
                
                const highlightedActions = behavior.shadowRoot.querySelector('highlighted-actions');
                if (!highlightedActions || !highlightedActions.shadowRoot) {
                    return null;
                }
                
                const expandable = highlightedActions.shadowRoot.querySelector('vt-ui-expandable');
                if (!expandable || !expandable.shadowRoot) {
                    return null;
                }
                
                const expandableEntry = expandable.querySelector('vt-ui-expandable-entry');
                if (!expandableEntry) {
                    return null;
                }
                
                const simpleExpandableList = expandableEntry.querySelector('vt-ui-simple-expandable-list');
                if (!simpleExpandableList) {
                    return null;
                }
                
                const listItems = simpleExpandableList.shadowRoot.querySelectorAll('li');
                if (listItems.length === 0) {
                    return null;
                }
                
                // Extract text from list items
                const sequences = Array.from(listItems).map(item => item.textContent.trim());
                return sequences.join(' ');
                
            } catch (error) {
                console.error('Error extracting behavior data:', error);
                return null;
            }
        """)
        
        return behavior_data
    except Exception as e:
        print(f"Error in get_behavior_data: {e}")
        return None

def get_malware_data():
    driver = get_chrome_driver()
    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    data = []
    
    for malware_family, hashes in hash_groups.items():
        print(f"\n🔍 Processing {malware_family} family ({len(hashes)} samples)")
        
        for i, md5 in enumerate(hashes):
            url = f'https://www.virustotal.com/gui/file/{md5}/behavior'
            print(f"[{malware_family}] {i+1}/{len(hashes)}. Scraping {md5}")
            
            try:
                behavior_url = f'https://www.virustotal.com/gui/file/{md5}/behavior'
                driver.get(behavior_url)
                
                print("⏳ Waiting for page to load...")
                time.sleep(15) 
                
                current_url = driver.current_url
                print(f"📍 Current URL: {current_url}")
                
                if 'captcha' in current_url.lower() or 'blocked' in current_url.lower():
                    print("🚫 Detected captcha/block. Waiting longer...")
                    time.sleep(60)
                    continue
                
                if not wait_for_element_to_exist(driver, 'vt-ui-shell', timeout=20):
                    print("❌ vt-ui-shell element not found")
                    continue
                
                print("✅ Main shell element found")
                
                sequence = get_behavior_data(driver)
                
                try : 
                    if sequence:
                        data.append({
                            "sequence": sequence,
                            "label": malware_family,
                            "md5": md5
                        })
                        print(f"✅ Successfully extracted data for {md5}")
                        print(data)
                    else :
                        print(data)
                        print(f"❌ No behavior data found for {md5}")
                        
                except Exception as e:
                    print(f"❌ No behavior data found for {md5}", e)
                
                time.sleep(2 + (i % 3))
                
            except Exception as e:
                print(f"❌ Error processing {md5}: {e}")
                continue
    
    driver.quit()
    return data

def save_checkpoint(data, filename="checkpoint.csv"):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"💾 Checkpoint saved with {len(data)} records")

if __name__ == "__main__":
    print("🚀 Starting VirusTotal scraping...")
    
    try:
        mal_data = get_malware_data()
        
        if mal_data:
            df = pd.DataFrame(mal_data)
            output_file = "ransom_scraping/virustotal_sequences_v3.csv"
            df.to_csv(output_file, index=False)
            print(f"✅ Data saved to {output_file}")
            print(f"📊 Total records: {len(mal_data)}")
            
            summary = df['label'].value_counts()
            print("\n📈 Summary by malware family:")
            for family, count in summary.items():
                print(f"  {family}: {count} samples")
        else:
            print("❌ No data was collected")
            
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")