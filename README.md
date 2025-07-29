1. Steps to Run the Test Suites in Less Than 2 mins

Create a Fresh Virtual Environment in any of your directories

Step 1:  C:\destroy>   python -m venv clean_env

Step 2:  C:\destroy>   cd clean_env

Step 3:  C:\destroy>clean_env\Scripts\activate

Step 4:  (clean_env) C:\destroy>  git clone https://github.com/onolunose/create_account_page.git

Step 5:  (clean_env) C:\destroy>  cd create_account_page\WordPress

RUN THE UI AND API TEST SUITES

Step 6:  (clean_env) C:\test_env\create_account_page\wordpress>  pytest tests/home/createAccount_tests.py -v --tb=short --disable-warnings -s  
 
Step 7:  (clean_env) C:\test_env\create_account_page\wordpress>  pytest tests/home/login_tests.py -v --tb=short --disable-warnings -s

Step 8:  (clean_env) C:\test_env\create_account_page\wordpress>  newman run api_tests/Verbatimly.postman_collection.json -e api_tests/Verbatimly_Environment.postman_environment.json

The End...

2. Project Structure
wordpress/
├── api_tests/
│   ├── Verbatimly.postman_collection.json
│   └── Verbatimly_Environment.postman_environment.json
├── base/
├── configfiles/
├── pages/home/
├── tests/home/
├── utilities/
├── requirements.txt
└── pytest.ini

3. Prerequisites
•	pip install -r requirements.txt
pytest==8.4.1
python-dotenv==1.1.1
selenium==4.34.2
webdriver-manager>=4.0.0


4. Run API Tests (Postman via Newman)
cd wordpress
newman run api_tests/Verbatimly.postman_collection.json \
  -e api_tests/Verbatimly_Environment.postman_environment.json

5. Run Selenium UI Tests (Pytest)
Login Tests
pytest tests/home/login_tests.py -v --tb=short --disable-warnings -s
Create Account Tests
pytest tests/home/createAccount_tests.py -v --tb=short --disable-warnings -s
6. Logs & Reports
•	Execution logs: automation.log 
•	Screenshot: Screenshot shows failed test screenshot
