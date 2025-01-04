import json
import pandas as pd

def parse_log_file(log_file_path: str, csv_file_path: str, output_json_path: str = None):
    """Parse TSP experiment log file and CSV metrics to extract population and status data."""
    # Read CSV file first
    metrics_df = pd.read_csv(csv_file_path)
    
    # Read and parse log file as before
    with open(log_file_path, 'r') as f:
        content = f.read()
    
    sections = content.split("Best sol:")
    
    data = []
    for section in sections[1:]:  # Skip first empty section
        # Parse status data
        status_lines = section.strip().split('\n')[:4]
        generation = int(status_lines[1].split(': ')[1])
        
        # Get variance from CSV for this generation
        variance = metrics_df[metrics_df['iteration'] == generation]['variance'].values[0]
        
        status = {
            'best_solution': float(status_lines[0]),
            'generation': generation,
            'temperature': float(status_lines[2].split(': ')[1]),
            'population_size': int(status_lines[3].split(': ')[1]),
            'variance': float(variance)  # Add variance to status
        }
        
        # Find the population data (list of tuples) in the previous section
        pop_start = sections[sections.index(section)-1].rfind('[([')
        if pop_start != -1:
            pop_end = sections[sections.index(section)-1].rfind(')]\n\n')
            pop_string = sections[sections.index(section)-1][pop_start:pop_end+2]
            population = eval(pop_string)
            
            data.append({
                'status': status,
                'population': population
            })
    
    # Convert population tuples to lists for JSON serialization
    json_data = []
    for gen in data:
        json_gen = {
            'status': gen['status'],
            'population': [list(route) for route in gen['population']]
        }
        json_data.append(json_gen)
    
    # Save to JSON file if output path is provided
    if output_json_path:
        with open(output_json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
    
    return json_data

if __name__ == '__main__':
    log_path = input("Enter the path to the log file: ")
    csv_path = input("Enter the path to the CSV file: ")
    json_path = input("Enter the path to save the output JSON file: ")
    
    experiment_data = parse_log_file(log_path, csv_path, json_path)
    print(f"Data saved to {json_path}")
    print(f"Number of generations: {len(experiment_data)}")
    print(f"Sample status data with variance: {experiment_data[0]['status']}")
