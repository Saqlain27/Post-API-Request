import requests

# === CONFIGURATION ===
name = "Mohammad Saqlain Shaikh"
reg_no = "0827AL221083"
email = "mohammadsaqlain221000@acropolis.in"

# === FINAL SQL QUERY ===
final_query = """
SELECT 
    P.AMOUNT AS SALARY,
    CONCAT(E.FIRST_NAME, ' ', E.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE, E.DOB) / 365) AS AGE,
    D.DEPARTMENT_NAME
FROM 
    PAYMENTS P
JOIN 
    EMPLOYEE E ON P.EMP_ID = E.EMP_ID
JOIN 
    DEPARTMENT D ON E.DEPARTMENT = D.DEPARTMENT_ID
WHERE 
    DAY(P.PAYMENT_TIME) != 1
ORDER BY 
    P.AMOUNT DESC
LIMIT 1;
"""

# === STEP 1: Generate Webhook ===
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
generate_payload = {
    "name": name,
    "regNo": reg_no,
    "email": email
}

print("Requesting webhook and token...")
generate_response = requests.post(generate_url, json=generate_payload)

if generate_response.status_code != 200:
    print("Failed to generate webhook:", generate_response.text)
    exit()

generate_data = generate_response.json()
webhook_url = generate_data["webhook"]
access_token = generate_data["accessToken"]

print("Received webhook URL and access token.")
print("Webhook:", webhook_url)

# === STEP 2: Submit SQL Query ===
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
submit_payload = {
    "finalQuery": final_query.strip()
}

print("Submitting SQL query...")
submit_response = requests.post(webhook_url, headers=headers, json=submit_payload)

# === Print Submission Status ===
print("Submission status code:", submit_response.status_code)
print("Response:")
print(submit_response.text)
