# sales_targets.py

import os
import pandas as pd
import random

def generate_sales_targets(sales_team, total_sales_target, new_clients_percentage):
    targets = []
    # Calculate targets based on the percentages
    new_clients_target = total_sales_target * (new_clients_percentage / 100)
    existing_clients_target = total_sales_target - new_clients_target

    # Distribute targets among sales team members
    for rep in sales_team:
        individual_total_target = round(total_sales_target / len(sales_team), 2)
        individual_new_target = round(new_clients_target / len(sales_team), 2)
        individual_existing_target = round(existing_clients_target / len(sales_team), 2)

        target = {
            'sales_rep_id': rep['employee_id'],
            'sales_rep_name': f"{rep['first_name']} {rep['last_name']}",
            'total_sales_target': individual_total_target,
            'new_clients_target': individual_new_target,
            'existing_clients_target': individual_existing_target
        }
        targets.append(target)

    # Save to CSV
    df_targets = pd.DataFrame(targets)
    df_targets.to_csv(os.path.join('data', 'sales_targets.csv'), index=False)

    print("Sales targets generated.")
    return targets