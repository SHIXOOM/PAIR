import json
import pandas as pd
import os

def parse_log_file(log_file_path: str, csv_file_path: str, output_json_path: str = None):
    """Parse TSP experiment log file and iterations csv to extract population and status data."""
    iterations_df = pd.read_csv(csv_file_path)
    
    with open(log_file_path, 'r') as f:
        log_content = f.read()
    
    sections = log_content.split("Best sol:")
    
    data = []
    for section in sections[1:]:  # skip first empty section
        # parse generation data
        status_lines = section.strip().split('\n')[:4]
        generation = int(status_lines[1].split(': ')[1])
        
        # Get variance from csv for this generation
        variance = iterations_df[iterations_df['iteration'] == generation]['variance'].values[0]
        
        generation_data = {
            'best_solution': float(status_lines[0]),
            'generation': generation,
            'temperature': float(status_lines[2].split(': ')[1]),
            'population_size': int(status_lines[3].split(': ')[1]),
            'variance': float(variance) 
        }
        
        # find the population data (list of tuples) in the previous section
        pop_start = sections[sections.index(section)-1].rfind('[([')
        if pop_start != -1:
            pop_end = sections[sections.index(section)-1].rfind(')]\n\n')
            pop_string = sections[sections.index(section)-1][pop_start:pop_end+2]
            population = eval(pop_string)
            
            data.append({
                'status': generation_data,
                'population': population
            })
    
    # convert population tuples to lists for JSON serialization
    json_data = []
    for gen in data:
        json_gen = {
            'status': gen['status'],
            'population': [list(route) for route in gen['population']]
        }
        json_data.append(json_gen)

    with open(output_json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    return json_data

if __name__ == '__main__':
    log_path = input("Enter the path to the log file: ")
    csv_path = input("Enter the path to the CSV file: ")
    json_file_name = input("Enter the name for the output JSON file (without extension): ")
    json_path = os.path.join(os.path.dirname(__file__), 'parsed-data', f"{json_file_name}.json")
    
    experiment_data = parse_log_file(log_path, csv_path, json_path)
    print(f"Data saved to {json_path}")
    print(f"Number of generations: {len(experiment_data)}")
    print(f"Sample status data with variance: {experiment_data[0]['status']}")
