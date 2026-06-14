import os
import pandas as pd
from pathlib import Path
import duckdb
import matplotlib.pyplot as plt

# Define Paths
DB_PATH = Path("data/output/sales.duckdb")
IMAGE_DIR = Path("docs/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_IMAGE = IMAGE_DIR / "regional_sales_summary.png"

def main():
    if not DB_PATH.exists():
        print(f"Error: Database file not found at {DB_PATH}. Please run your consumer first!")
        return

    print("Connecting to DuckDB to extract live streaming metrics...")
    # Query the valid sales table aggregated by region
    query = """
        SELECT region_id, COUNT(*) AS sale_count
        FROM consumed_valid_sales
        GROUP BY region_id
        ORDER BY sale_count DESC
    """
    
    with duckdb.connect(str(DB_PATH)) as conn:
        df = conn.execute(query).df()

    if df.empty:
        print("The database is currently empty. Start your producer and consumer streams first!")
        return

    print("Generating professional bar chart...")
    
    # Configure professional plot styling
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Generate sorted bars
    bars = ax.bar(df['region_id'], df['sale_count'], color='#3498db', edgecolor='#2980b9', width=0.6)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Title and Labels
    ax.set_title("Live Stream Event Distribution by Region", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Region Identifier", fontsize=11, labelpad=10)
    ax.set_ylabel("Total Valid Messages Stored", fontsize=11, labelpad=10)
    
    # Clean up margins so nothing is truncated
    plt.tight_layout()
    
    # Save chart to the docs directory
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    plt.close()
    
    print(f"Success! Graph saved beautifully to: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()