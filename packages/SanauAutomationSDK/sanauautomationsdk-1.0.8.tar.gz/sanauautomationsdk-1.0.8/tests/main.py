from src.SanauAutomationSDK.SanauAutomationSDK import SanauAutomationSDK
sasdk = SanauAutomationSDK('KZ', 'dev-1.pbo.kz', '7nuLUYDYeQLyd3Rn')

# print(sasdk.oked.get_all_okeds({'API-ACCESS-TOKEN': 'f6f9e9272531a31defdbb4ea778b3997'}))

# print(sasdk.oked.get_all_okeds())

try:
    print(sasdk.client.get_db_employees(db_name='pbo-test'))
    # print(sasdk.oked.get_all_okeds())
except Exception as e:
    print("EXCEPTION!!! ", e)

