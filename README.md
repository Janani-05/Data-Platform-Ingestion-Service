# Data Platform Ingestion Service

##  Deliverable 1: Understanding the Platform Design

### ️ Architecture Diagram

(GCS Bucket: your-project-uploads)
 |  [Trigger: metadata.json upload]
(Cloud Function: gcs-to-bq-ingestor)
|
Reads metadata- Creates BigQuery Dataset/Table- Loads data.csv
| 
(BigQuery: sales_analytics.daily_leads_v1)



### ️ Technology Justification

**Google Cloud Storage (GCS):**  
Used as a centralized location for analytics teams to upload batch files (CSV and metadata). GCS triggers events when files are uploaded, allowing automation of the ingestion pipeline.

**Google Cloud Functions:**  
A serverless compute platform that automatically executes the ingestion logic when triggered by file uploads, eliminating the need to manage servers.

**BigQuery:**  
A scalable data warehouse where the ingested datasets are stored for analysis and reporting. Ideal for handling large-scale data analytics workloads.

---

##  Deliverable 2: Coding Challenge – Automated Ingestion Service

The Cloud Function (`main.py`) performs the following actions:

1. Triggered when a `metadata.json` file is uploaded to a GCS bucket.  
2. Reads and parses the metadata.  
3. Idempotently creates the target BigQuery dataset and table.  
4. Loads the associated `data.csv` into the BigQuery table.  
5. Sets table description and labels for governance.

###  Example Workflow

1. **User uploads two files** into a GCS bucket:  
   - `metadata.json` (contains schema and table details)  
   - `data.csv` (contains the actual data)  
2. **Cloud Function runs automatically**.  
3. It reads the metadata, creates the dataset/table in BigQuery (if not already present), and loads the data.  
4. Data is now available for querying in BigQuery under the defined dataset.

---

### Deliverable 3: CI/CD and DevOps

The repository includes:
- **Terraform scripts** (`/terraform`) to define core infrastructure:
  - GCS bucket  
  - Cloud Function  
  - IAM permissions  
- **GitHub Actions workflow** (`.github/workflows/ci.yml`) automating:
  1. Python linting and unit testing  
  2. Terraform validation

###  Example CI/CD Flow

1. Developer commits code to the `main` branch.  
2. GitHub Actions automatically run tests and validate Terraform configuration.  
3. Upon success, Terraform can be applied to deploy the Cloud Function and other resources to GCP.  

This ensures **infrastructure as code**, **version control**, and **automated testing** for a consistent DevOps workflow.

---

### Deliverable 4: AI Usage Log

**My Goal:** I needed to mock BigQuery client in pytest.  
**My Prompt to AI:** “How do I use unittest.mock to simulate BigQuery client in pytest?”  
**AI's Raw Output:**
```python
from unittest.mock import MagicMock
mock_bq = MagicMock()
mock_bq.load_table_from_uri.return_value = None


