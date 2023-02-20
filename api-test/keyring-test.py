import keyring

x = keyring.get_password("alma_api", "alx_prod")
print(x)