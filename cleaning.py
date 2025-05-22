import pandas as pd
import re

df = pd.read_csv('ransom_scraping/virustotal_sequences_v3.csv')
# df = pd.read_csv('dataset_feature\sequence\pseudo_sequence_mal_dataset.csv')


df_cleaned = df[~df['sequence'].str.contains(r'#218|#217')]
df_cleaned = df_cleaned.drop_duplicates(subset='md5')

def clean_underscored_services(text):
    text = re.sub(r'(net\s+)?stop\s+"([^"]+)"', lambda m: 'Stop' + re.sub(r'\s+', '', m.group(2)), text, flags=re.IGNORECASE)
    text = re.sub(r'(net\s+)?stop\s+([^\s"]+)', lambda m: 'Stop' + m.group(2), text, flags=re.IGNORECASE)
    return text

def normalize_exec(text):
    text = re.sub(r'"?C:\\Windows\\[^\\"]+\\([^\\"]+)\.exe"?', lambda m: m.group(1).split('.')[0].capitalize(), text, flags=re.IGNORECASE)
    text = re.sub(r'"?C:\\Users\\[^\\"]+\\([^\\"]+)\.hta"?', lambda m: 'OpenHTA', text, flags=re.IGNORECASE)
    return text

def normalize_filepaths(text):
    # Untuk file HTA
    text = re.sub(r'"?C:\\Users\\[^\\"]+\\[^\\"]+\.hta"?', 'OpenHTAFile', text, flags=re.IGNORECASE)
    # Untuk file TXT
    text = re.sub(r'"?C:\\Users\\[^\\"]+\\[^\\"]+\.txt"?', 'OpenTxtFile', text, flags=re.IGNORECASE)
    return text

def normalize_malicious_cmd(text):
    # Taskkill + ping + delete
    text = re.sub(
        r'cmd\.exe.*taskkill\s+/f\s+/im.*del.*exit',
        'KillAndDeleteCommand',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(cmd\.exe|["\']?C:\\Windows\\system32\\exe["\']?)\s*/d\s*/c\s*taskkill\s*/f\s*/im[^&]*(&|&&).*del[^&]*(&|&&).*exit',
        'KillAndDeleteCommand',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'taskkill\s*/f\s*/im[^&]*(&|&&).*del[^&]*(&|&&).*exit',
        'KillAndDeleteCommand',
        text,
        flags=re.IGNORECASE
    )
    text =  re.sub(
        r'delete\s+shadows\s*/all\s*/quiet',
        'DeleteShadowsAllQuiet',
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'start\s+start\s+users\s+users',
        'StartUsers',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'config\s+workstation',
        'ConfigWorkstation',
        text,
        flags=re.IGNORECASE
    )
    return text

df_cleaned['sequence'] = (
    df_cleaned['sequence']
    .str.replace(r'\b\w+\.', '', regex=True)  # hapus awalan dll seperti kernel32.
    .str.replace(r'arp -A', '', regex=True)
    .str.replace(r'hostname', '', regex=True)
    .str.replace(r'ipconfig /all', '', regex=True)
    .str.replace(r'\s+', ' ', regex=True)  
    .str.strip()
    .apply(clean_underscored_services)
    .apply(normalize_exec)
    .apply(normalize_filepaths)
    .apply(normalize_malicious_cmd)
)

df_cleaned.to_csv('dataset_feature/add_ransom_cleaned/additional_ransome_new_no_duplicate.csv', index=False)
# df_cleaned.to_csv('dataset_feature/cleaned/pseudo_sequence_mal_cleaned.csv', index=False)

print("Cleaning selesai. Data disimpan di additional_ransome_new.csv")
