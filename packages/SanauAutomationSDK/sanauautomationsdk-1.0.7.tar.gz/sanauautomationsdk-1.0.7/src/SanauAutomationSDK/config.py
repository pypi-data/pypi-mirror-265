# GET
ONE_S_DATABASES = 'https://{domain}/botapi/v1/one_s/databases'
ARM_EMPLOYEES = 'https://{domain}/botapi/v1/one_s/databases/{db_name}/employees'
FILE_VAULT_DOWNLOAD_FILE = 'https://files.{domain}/download/file'
NATIONAL_BANK = 'https://nationalbank.kz/rss/get_rates.cfm?fdate={currency_date}'
OGD_EXCEL = 'https://kgd.gov.kz/sites/default/files/spravochniki/spravochnik_kodifikator_s_ukazaniem_bin_i_rekvizitami_dlya_zachisleniya_platezhey_v_byudzhet_po_organam_gosudarstvennyh_dohodov_respubliki_kazahstan.xlsx'
DOMAINS = 'https://auth.sanau.kz/domains_without_devs'
GET_ALERT = 'https://{domain}/botapi/v1/alert'
OKEDS = 'https://{domain}/api/v3/python_integration/get_all_okeds'

# POST
POST_ALERTS = 'https://{domain}/botapi/v1/alerts'
FETCH_TAXATION_ORGANS = 'https://{domain}/api/v3/python_integration/fetch_taxation_organs'

# PUT
RESOLVE_ALERT = 'https://{domain}/botapi/v1/alerts/resolve'

# DELETE
RESOLVE_ALL_ALERTS = 'https://{domain}/botapi/v1/alerts/resolve_all'
