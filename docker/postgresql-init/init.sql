
--
CREATE DATABASE mlflow;
CREATE USER mlflow WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;


--
CREATE DATABASE mlops;
CREATE USER airbyte WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO airbyte;
ALTER DATABASE mlops OWNER TO airbyte;

GRANT ALL ON SCHEMA public TO airbyte;
GRANT USAGE ON SCHEMA public TO airbyte;

CREATE SCHEMA raw_data;
GRANT ALL ON SCHEMA raw_data TO airbyte;
GRANT USAGE ON SCHEMA raw_data TO airbyte;

CREATE SCHEMA processed_data;
GRANT ALL ON SCHEMA processed_data TO airbyte;
GRANT USAGE ON SCHEMA processed_data TO airbyte;
