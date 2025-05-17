import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import get_chrome_driver
from hash_mal import hash_groups




def expand_shadow_element(driver, element):
    """Expand a shadow DOM element."""
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def behavior_tab(driver):

    try : 
        main_shell =  expand_shadow_element(driver, driver.find_element(By.TAG_NAME, 'vt-ui-shell'))
        file_shell = expand_shadow_element(driver, main_shell.find_element(By.TAG_NAME, 'file-view'))
        report_shell = expand_shadow_element(file_shell.find_element(By.TAG_NAME, 'vt-ui-main-generic-report'))
        tab_list = report_shell.find_elements(By.CSS_SELECTOR, 'div > div:nth-child(3) > div > ul > li')
        if not tab_list or len(tab_list) < 7:
            print("Tab list not ready")
            return None
        
        behavior_tab = tab_list[6]
        behavior_tab.click()
    except Exception as e:
        print(f"Failed to click behavior tab: {e}")
        return None

def get_malware_data():

    driver = get_chrome_driver()

    data = []

    for malware_family, hash in hash_groups.items() :
        for i, md5 in enumerate(hash) :

            url = f'https://www.virustotal.com/gui/file/{md5}/behavior'
            print(f"[{malware_family}] {i+1}. Scraping {md5}")

            driver.get(url)
            time.sleep(10)
                
            tab_clicked = 0

            for tab_clicked in range(5):
                try : 
                    behavior_tab(driver)
                    time.sleep(5)
                    continue
                      # Coba maksimal 5 kali
                except Exception as e:
                    print(f"Failed to click behavior tab: {e}")
                    time.sleep(5)
                    break
            
            try :
                main_shell =  expand_shadow_element(driver, driver.find_element(By.TAG_NAME, 'vt-ui-shell'))
                file_shell = expand_shadow_element(driver, main_shell.find_element(By.TAG_NAME, 'file-view'))
                report_shell = expand_shadow_element(file_shell.find_element(By.TAG_NAME, 'vt-ui-main-generic-report'))
                behavior_shell = expand_shadow_element(report_shell.find_element(By.TAG_NAME, 'vt-ui-file-behaviours'))
                ui_behaviour_shell = expand_shadow_element(behavior_shell.find_element(By.TAG_NAME, 'vt-ui-behaviour'))
                highlighted_actions_shell = expand_shadow_element(ui_behaviour_shell.find_element(By.TAG_NAME, 'highlighted-actions'))
                expandable_shell = expand_shadow_element(highlighted_actions_shell.find_element(By.TAG_NAME, 'vt-ui-expandable'))
                expandable_entry_shell = expand_shadow_element(expandable_shell.find_element(By.TAG_NAME, 'vt-ui-expandable-entry'))
                simple_expandable_list_shell = expand_shadow_element(expandable_entry_shell.find_element(By.TAG_NAME, 'vt-ui-simple-expandable-list'))
                list_items = simple_expandable_list_shell.find_elements(By.TAG_NAME, 'li')
                if list_items:
                    print(f"List items found: {len(list_items)}")
                    sequence = " ".join([item.text for item in list_items])
                    data.append({"sequence": sequence, "label": malware_family})
                else: 
                    print(f"No list items found for {md5}")
            except Exception as e:
                print(f"Failed to find elements: {e}")
                break

    driver.quit()
    return data

if __name__ == "__main__":
    mal_data = get_malware_data()
    df = pd.DataFrame(mal_data)
    df.to_csv("ransom_scraping/virustotal_sequences.csv", index=False)
    print("📁 Data disimpan ke virustotal_sequences.csv")
        
