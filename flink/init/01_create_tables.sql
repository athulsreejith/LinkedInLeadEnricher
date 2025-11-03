CREATE TABLE IF NOT EXISTS salesforce_contacts (
  id STRING,
  first_name STRING,
  last_name STRING,
  company STRING,
  email STRING
) WITH (
  'connector'='kafka',
  'topic'='salesforce_contacts',
  'properties.bootstrap.servers'='kafka:9092',
  'scan.startup.mode'='earliest-offset',
  'format'='json'
);

CREATE TABLE IF NOT EXISTS salesforce_myleads (
  full_name STRING,
  company STRING,
  email STRING
) WITH (
  'connector'='kafka',
  'topic'='salesforce_myleads',
  'properties.bootstrap.servers'='kafka:9092',
  'format'='json'
);

CREATE TABLE IF NOT EXISTS salesforce_icebreakers (
  full_name STRING,
  company STRING,
  summary STRING,
  facts ARRAY<STRING>,
  interest_topic STRING,
  icebreakers ARRAY<STRING>
) WITH (
  'connector'='kafka',
  'topic'='salesforce_icebreakers',
  'properties.bootstrap.servers'='kafka:9092',
  'format'='json'
);
