import json

# Utility module to import sensitive data from constans.json
# See also --environment-secrets pytest option

with open("constants.json") as f:
    data = json.load(f)
    test_email = data["test_email"]
    test_password = data["test_password"]
    login_page_url = data["login_page_url"]
    landing_page_url = data["landing_page_url"]