# Test cases

Run with `python -m unittest discover -s tests -v`. Actual results below reflect the recorded local test run.

| ID | Steps | Expected result | Actual result |
|---|---|---|---|
| TC-01 | Initialize temporary database | Schema and sample departments exist | Passed (`test_database_initializes_and_seeds_departments`) |
| TC-02 | Create administrator; try correct and incorrect passwords | Correct succeeds, incorrect fails | Passed (`test_admin_hash_auth`) |
| TC-03 | Create, search, update and delete employee | CRUD and search succeed | Passed (`test_employee_create_search_update_delete`) |
| TC-04 | Save employee with missing required field | Validation rejects input | Passed (`test_required_validation_and_duplicate_email`) |
| TC-05 | Insert duplicate email | Unique constraint rejects duplicate | Passed (`test_required_validation_and_duplicate_email`) |
| TC-06 | Delete department in use | Operation is rejected | Passed (`test_department_in_use_and_duplicate`) |
| TC-07 | Export employee list and inspect dashboard counts | CSV contains row; counts match records | Passed (`test_csv_and_dashboard`) |

Execution summary: 6 unittest methods passed; 0 failed. Run on Python 3.14 in this workspace with `python -m unittest discover -s tests -v`. UI workflows are not covered by this headless service test suite.
