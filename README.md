# Synthetic Data Generator

The Synthetic Data Generator is a Python-based tool designed to create realistic synthetic datasets for various departments of a fictional SaaS cloud service provider. This tool is ideal for testing, development, or educational purposes without compromising any real personal or sensitive information.

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
- **Human Resources Data**: Creates detailed employee records, including personal details, job information, payroll data, and performance reviews.
- **Sales Data**: Generates sales opportunities, customers, sales targets, and email conversations replicating CRM data.
- **Support Data**: Creates support tickets and issue summaries linked to customers.
- **Finance Data**: Generates invoices, transactions, accounts payable, financial reports, and MRR files replicating accounting software data.
- **Marketing Data**: Produces marketing campaigns, leads, and a company brand book similar to marketing automation tools.
- **Knowledge Base**: Generates knowledge base articles on various topics relevant to the company.

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
- `--account_executive_count`: Number of Account Executives (default: 50)
- `--num_opportunities`: Number of sales opportunities (default: 200)
- `--total_sales_target`: Total sales target (default: 6000000)
- `--new_clients_percentage`: Percentage of sales target from new clients (default: 75.0)
- `--international_clients_percentage`: Percentage of international clients (default: 30.0)

### Example

```bash
python main.py --employee_count 150 --account_executive_count 30 --num_opportunities 100
```

## Configuration

You can adjust various parameters to tweak the generated data:

- **Employee Count**: Adjust the total number of employees to generate.
- **Account Executive Count**: Set the number of Account Executives in the sales team.
- **Sales Opportunities**: Define how many sales opportunities to create.
- **Sales Targets**: Set the total sales target and the percentage expected from new clients.
- **International Clients**: Specify the percentage of clients that are international.

These parameters can be modified via command-line arguments when running the `main.py` script.

## Generated Data

The generated data files are saved in the `data` directory:

- `employees.csv`
- `customers.csv`
- `opportunities.csv`
- `sales_targets.csv`
- `support_tickets.csv`
- `invoices.csv`
- `transactions.csv`
- `accounts_payable.csv`
- `rolling_forecast.csv`
- `mrr.csv`
- `campaigns.csv`
- `leads.csv`
- `knowledge_base.csv`
- `brandbook.txt`

## Dependencies

- Python 3.7 or higher
- See `requirements.txt` for a full list of Python packages.

## Notes

- **OpenAI API Usage**: This tool uses the OpenAI API to generate realistic text content. Be mindful of the API usage limits and associated costs. It's recommended to monitor your usage in your OpenAI account.
- **Asynchronous Execution**: The script uses asynchronous programming to improve performance. Ensure your Python version supports the `asyncio` features used in the scripts.
- **Logging**: The tool generates log files for each module to help with debugging and monitoring.
- **Error Handling**: Extensive error handling has been implemented to ensure smooth execution.
- **Rate Limiting**: Be cautious of API rate limits. The script includes mechanisms to handle rate limiting, but adjust the concurrency settings if necessary.
