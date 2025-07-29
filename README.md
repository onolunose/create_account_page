1. Project Structure
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

2. Prerequisites
•	pip install -r requirements.txt
pytest==8.4.1
python-dotenv==1.1.1
selenium==4.34.2
webdriver-manager>=4.0.0


3. Run API Tests (Postman via Newman)
cd wordpress
newman run api_tests/Verbatimly.postman_collection.json \
  -e api_tests/Verbatimly_Environment.postman_environment.json

4. Run Selenium UI Tests (Pytest)
Login Tests
pytest tests/home/login_tests.py -v --tb=short --disable-warnings -s
Create Account Tests
pytest tests/home/createAccount_tests.py -v --tb=short --disable-warnings -s
5. Logs & Reports
•	Execution logs: automation.log 
•	Screenshot: Screenshot shows failed test screenshot
