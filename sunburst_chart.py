import pandas as pd
import plotly.express as px

# 1. Load the data
# Replacing missing values (NaN) with empty strings for easier processing
df = pd.read_csv('data.csv').fillna('')

# 2. Clean and structure the hierarchy
current_stage = ""
structured_data = []

for index, row in df.iterrows():
    item = str(row['Technology/Machinery ']).strip()
    cost = row['Cost Incurred (USD Thousands)']
    
    # Skip completely empty rows
    if not item:
        continue
        
    # If the row defines a major Stage (e.g., "Stage1 - ..."), update our tracker
    if "Stage" in item:
        current_stage = item
    else:
        # If it's a technology/machinery under a stage, save it to our list
        # Only keep rows that have a valid cost to map size accurately
        if current_stage and cost != '':
            structured_data.append({
                'Stage': current_stage,
                'Technology': item,
                'Cost': float(cost)
            })

# Convert our cleaned list back into a clean DataFrame
clean_df = pd.DataFrame(structured_data)

# 3. Create the Sunburst Chart
# path=['Stage', 'Technology'] creates the multi-layered rings
# values='Cost' makes the size of each slice proportional to its budget/cost
fig = px.sunburst(
    clean_df, 
    path=['Stage', 'Technology'], 
    values='Cost',
    title="Battery Supply Chain Analysis: Cost Breakdown by Stage",
    color='Stage', # Automatically color-code by major processing stage
    template='plotly_white'
)

# Optimize text layout inside the chart rings
fig.update_traces(textinfo="label+percent parent")

# 4. Save the interactive visualization as an HTML file
fig.write_html('sunburst_chart.html')
print("Sunburst chart successfully generated as 'sunburst_chart.html'!")
