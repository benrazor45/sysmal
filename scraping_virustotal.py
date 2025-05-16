import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import get_chrome_driver
from hash_mal import hash_groups

def get_malware_data():

    driver = get_chrome_driver()

    data = []

    for malware_family, hash in hash_groups.items() :
        for i, md5 in enumerate(hash) :

            url = f'https://www.virustotal.com/gui/file/{md5}/behavior'
            print(f"[{malware_family}] {i+1}. Scraping {md5}")

            driver.get(url)
            time.sleep(10)

            # WebDriverWait(driver, 20).until(lambda d: d.execute_script("""
            #     return document.querySelector('vt-ui-shell')?.shadowRoot
            # """) is not null)
            tab_clicked = False
            # for _ in range(5): 
            #     try :
            #         click_behaviour_tab =  """
            #         let shell = document.querySelector('vt-ui-shell').shadowRoot;
            #         let fileView = shell.querySelector('file-view').shadowRoot;
            #         let report = fileView.querySelector('vt-ui-main-generic-report').shadowRoot;
            #         let tab = report.querySelectorAll('div > div:nth-child(3) > div > ul > li')[6];
            #         if (tab) {
            #             let anchor = tab.querySelector('a');
            #             if (anchor) {
            #                 anchor.click();
            #                 return 'Tab Behavior clicked';
            #             }
            #         }
            #         return 'Behavior tab not found';
            #         """
            #         result = driver.execute_script(click_behaviour_tab)
            #         print(result)
            #         time.sleep(5)
            #     except Exception as e:
            #         print(f"Failed to click bheavior tab {e}")
            #         continue

            for _ in range(5):  # Coba maksimal 5 kali
                try:
                    result = driver.execute_script("""
                        try {
                            let shell = document.querySelector('vt-ui-shell')?.shadowRoot;
                            if (!shell) return 'shell not ready';
                            let fileView = shell.querySelector('file-view')?.shadowRoot;
                            if (!fileView) return 'fileView not ready';
                            let report = fileView.querySelector('vt-ui-main-generic-report#report')?.shadowRoot;
                            if (!report) return 'report not ready';

                            let tabList = report.querySelectorAll('div > div:nth-child(3) > div > ul > li');
                            if (!tabList || tabList.length < 7) return 'tab list not ready';

                            let tab = tabList[6];
                            let anchor = tab?.querySelector('a');
                            if (!anchor) return 'anchor not found';

                            anchor.click();
                            return 'clicked';
                        } catch(e) {
                            return 'error: ' + e;
                        }
                    """)
                    print("Tab behavior status:", result)
                    if result == "clicked":
                        tab_clicked = True
                        break
                    else:
                        time.sleep(2)  # Tunggu dan ulangi
                except Exception as e:
                    print(f"Gagal klik tab Behavior: {e}")
                    time.sleep(2)

            if not tab_clicked:
                print(f"Gagal menemukan tab behavior setelah beberapa kali percobaan. Lewati.")
                continue
            time.sleep(5) 

            javascript = """
            return Array.from(
                document
                    .querySelector('vt-ui-shell').shadowRoot
                    .querySelector('file-view').shadowRoot
                    .querySelector('vt-ui-main-generic-report').shadowRoot
                    .querySelector('vt-ui-file-behaviours').shadowRoot
                    .querySelector('vt-ui-behaviour').shadowRoot
                    .querySelector('highlighted-actions').shadowRoot
                    .querySelector('vt-ui-expandable').shadowRoot
                    .querySelector('vt-ui-expandable-entry').shadowRoot
                    .querySelector('vt-ui-simple-expandable-list').shadowRoot
                    .querySelectorAll('li')
            ).map(el => el.textContent.trim());
            """
            try:
                api_calls = driver.execute_script(javascript)
                print(api_calls)
                if api_calls :
                    sequence = " ".join(api_calls)
                    data.append({"sequence": sequence, "label": malware_family})
                    print(f"API calls found ({len(api_calls)}): {api_calls[:5]}...")
                else :
                    print(f"No API calls for {md5}")
            except Exception as e:
                print(f"[{malware_family}] {i+1}. Failed to take api calls: {e}")
                api_calls = []

    driver.quit()
    return data

if __name__ == "__main__":
    mal_data = get_malware_data()
    df = pd.DataFrame(mal_data)
    df.to_csv("ransom_scraping/virustotal_sequences.csv", index=False)
    print("📁 Data disimpan ke virustotal_sequences.csv")
        
