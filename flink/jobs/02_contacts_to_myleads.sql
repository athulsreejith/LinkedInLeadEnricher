INSERT INTO salesforce_myleads
SELECT
  CONCAT_WS(' ', first_name, last_name) AS full_name,
  company,
  email
FROM salesforce_contacts;
