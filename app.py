import requests
import json

# Constants
GENERATE_WEBHOOK_URL = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
TEST_WEBHOOK_URL = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"

# Function to generate webhook
def generate_webhook():
   payload = {
       "name": "John Doe",
       "regNo": "852",
       "email": "john@example.com"
   }
   response = requests.post(GENERATE_WEBHOOK_URL, json=payload)
   return response.json()

# Function to solve SQL problem based on regNo
def solve_sql_problem(reg_no):
   last_digit = int(reg_no[-1])
   if last_digit % 2 == 1:  # Odd
       # Logic for Question 1
       final_query = """
        SELECT 
            p.AMOUNT AS SALARY,
            CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
            FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365.25) AS AGE,
            d.DEPARTMENT_NAME
        FROM PAYMENTS p
        JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
        JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
        WHERE DAY(p.PAYMENT_TIME) != 1
          AND p.AMOUNT = (
            SELECT MAX(AMOUNT)
            FROM PAYMENTS
            WHERE DAY(PAYMENT_TIME) != 1
        )
        """
   else:  # Even
       # Logic for Question 2
       final_query = """
        SELECT 
            e1.EMP_ID,
            e1.FIRST_NAME,
            e1.LAST_NAME,
            d.DEPARTMENT_NAME,
            COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
        FROM EMPLOYEE e1
        JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
        LEFT JOIN EMPLOYEE e2 
            ON e1.DEPARTMENT = e2.DEPARTMENT 
            AND e2.DOB > e1.DOB
        GROUP BY 
            e1.EMP_ID, 
            e1.FIRST_NAME, 
            e1.LAST_NAME, 
            d.DEPARTMENT_NAME
        ORDER BY 
            e1.EMP_ID DESC;
        """
   return final_query

# Function to submit the final SQL query
def submit_solution(webhook_url, access_token, final_query):
   headers = {
       "Authorization": access_token,
       "Content-Type": "application/json"
   }
   payload = {
       "finalQuery": final_query
   }
   response = requests.post(webhook_url, headers=headers, json=payload)
   return response.json()

# Main function
def main():
   # Step 1: Generate webhook
   response = generate_webhook()
   webhook_url = response['webhook']
   access_token = response['accessToken']
   reg_no = "852"  # Example registration number

   # Step 2: Solve SQL problem
   final_query = solve_sql_problem(reg_no)

   # Step 3: Submit the solution
   result = submit_solution(webhook_url, access_token, final_query)
   print(result)

if __name__ == "__main__":
   main()
