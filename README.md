# Synthetic Data Generator

The Synthetic Data Generator is a Python-based tool designed to create realistic synthetic datasets and documents for various departments of a fictional SaaS cloud service provider, **Advanced Cloud**. This tool is ideal for testing, development, or educational purposes without compromising any real personal or sensitive information.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Generated Data](#generated-data)
- [Dependencies](#dependencies)
- [Notes](#notes)
- [License](#license)

## Features

- **Company Information**: Generates random company names, services, and mission statements.
- **Human Resources Data**: Creates detailed employee records, including personal details, job information, payroll data, performance reviews, and organizational charts.
- **Sales Data**: Generates sales opportunities, customers, sales targets, sales plans, and email conversations replicating CRM data.
- **Support Data**: Creates support tickets and issue summaries linked to customers.
- **Finance Data**: Generates invoices, transactions, accounts payable, financial reports, and MRR files replicating accounting software data.
- **Marketing Data**: Produces marketing campaigns, leads, and a company brand book similar to marketing automation tools.
- **Knowledge Base**: Generates knowledge base articles on various topics relevant to the company.
- **Documents**: Generates documents such as sales plans and Account Executive handbooks in multiple formats (TXT, DOCX, PDF).
- **Organizational Charts**: Creates detailed organizational charts in multiple formats (TXT, DOCX, PDF).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Synthetic-Data-Generator.git
   cd Synthetic-Data-Generator
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up OpenAI API Key**

   The tool uses the OpenAI API to generate realistic text data. You need to obtain an API key from OpenAI and set it as an environment variable.

   - **On Windows:**

     ```bash
     set OPENAI_API_KEY=your-api-key-here
     ```

   - **On macOS/Linux:**

     ```bash
     export OPENAI_API_KEY=your-api-key-here
     ```

## Usage

Run the main script with optional command-line arguments to customize data generation.

```bash
python main.py [options]
```

### Options

- `--employee_count`: Number of employees to generate (default: 200)
- `--num_opportunities`: Number of sales opportunities (default: 200)
- `--total_sales_target`: Total sales target (default: 10000000)
- `--new_clients_percentage`: Percentage of sales target from new clients (default: 60.0)
- `--international_clients_percentage`: Percentage of international clients (default: 30.0)

### Example

```bash
python main.py --employee_count 150 --num_opportunities 100
```

## Configuration

You can adjust various parameters to tweak the generated data:

- **Employee Count**: Adjust the total number of employees to generate.
- **Sales Opportunities**: Define how many sales opportunities to create.
- **Sales Targets**: Set the total sales target and the percentage expected from new clients.
- **International Clients**: Specify the percentage of clients that are international.

These parameters can be modified via command-line arguments when running the `main.py` script.

## Generated Data

The generated data files are saved in the `data` directory:

- **Employee Data**:
  - `employees.csv`
  - `hr_records.docx`
- **Organizational Chart**:
  - `org_chart.txt`
  - `org_chart.docx`
  - `org_chart.pdf`
- **Sales Data**:
  - `opportunities.csv`
  - `sales_targets.csv`
- **Sales Plan**:
  - `sales_plan.txt`
  - `sales_plan.docx`
  - `sales_plan.pdf`
- **Account Executive Handbook**:
  - `ae_handbook.docx`
  - `ae_handbook.pdf`
- **Support Tickets**:
  - `support_tickets.csv`
- **Finance Data**:
  - `invoices.csv`
  - `transactions.csv`
  - `accounts_payable.csv`
  - `rolling_forecast.csv`
  - `mrr.csv`
- **Marketing Data**:
  - `campaigns.csv`
  - `leads.csv`
  - `brandbook.txt`
- **Knowledge Base**:
  - `knowledge_base.csv`

## Dependencies

- Python 3.7 or higher
- See `requirements.txt` for a full list of Python packages.

## Notes

- **OpenAI API Usage**: This tool uses the OpenAI API to generate realistic text content. Be mindful of the API usage limits and associated costs. It's recommended to monitor your usage in your OpenAI account.
- **Asynchronous Execution**: The script uses asynchronous programming to improve performance. Ensure your Python version supports the `asyncio` features used in the scripts.
- **Logging**: The tool generates log files for each module to help with debugging and monitoring.
- **Error Handling**: Extensive error handling has been implemented to ensure smooth execution.
- **Rate Limiting**: Be cautious of API rate limits. The script includes mechanisms to handle rate limiting, but adjust the concurrency settings if necessary.
- **Document Generation**: Generated documents are available in TXT, DOCX, and PDF formats for versatility and ease of use.
- **Organizational Structure**: Ensure that employee data includes necessary fields like `manager_id` and `manager_name` for accurate organizational chart generation.
