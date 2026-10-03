"""MAP Longitudinal Growth Tracking and Prediction.

Calculates year-by-year Fall-to-Spring growth from 2021 to 2026,
and predicts the Spring 2027 cohort average based on historical trends.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def load_growth_data(data_dir: Path) -> pd.DataFrame:
    """Load all 6 years of growth Excel files and calculate cohort averages."""
    files = {
        "2021-2022": data_dir / "MAP Growth Data 2021_2022.xlsx",
        "2022-2023": data_dir / "MAP Growth Data 2022_2023.xlsx",
        "2023-2024": data_dir / "MAP Growth Data 2023_2024.xlsx",
        "2024-2025": data_dir / "MAP Growth Data 2024_2025.xlsx",
        "2025-2026": data_dir / "MAP Growth Data 2025_2026.xlsx",
        "2026-2027": data_dir / "MAP Growth Data 2026_2027.xlsx",
    }

    yearly_stats = []

    for year, file_path in files.items():
        if not file_path.exists():
            print(f"Warning: {file_path.name} not found. Skipping...")
            continue
            
        df = pd.read_excel(file_path)
        
        # Clean up unpredictable column spaces (e.g., "Spring  RitScore")
        df.columns = [c.replace('  ', ' ').strip() for c in df.columns]

        # Calculate averages for Fall and Spring
        fall_mean = df['Fall RitScore'].mean() if 'Fall RitScore' in df.columns else np.nan
        spring_mean = df['Spring RitScore'].mean() if 'Spring RitScore' in df.columns else np.nan
        
        # Calculate actual growth if both exist
        growth = spring_mean - fall_mean if pd.notna(fall_mean) and pd.notna(spring_mean) else np.nan
        
        yearly_stats.append({
            'Year': year, 
            'Fall_Avg': fall_mean, 
            'Spring_Avg': spring_mean, 
            'Growth': growth
        })

    return pd.DataFrame(yearly_stats)


def analyze_and_plot(df: pd.DataFrame, output_path: Path):
    """Print the historical growth analysis, predict 2027, and save a chart."""
    # Split the historical data from the current incomplete year
    history = df.dropna(subset=['Growth'])
    current_year = df[df['Growth'].isna()].copy()
    
    print("\n==================================================")
    print("  YEAR-BY-YEAR FALL TO SPRING GROWTH")
    print("==================================================")
    for _, row in history.iterrows():
        print(f"{row['Year']}: Grew by {row['Growth']:.2f} points (Fall: {row['Fall_Avg']:.2f} -> Spring: {row['Spring_Avg']:.2f})")
        
    # Calculate historical average growth
    avg_historical_growth = history['Growth'].mean()
    
    # Predict Spring 2027
    predicted_spring = current_year['Fall_Avg'].values[0] + avg_historical_growth
    
    print("\n==================================================")
    print("  SPRING 2027 PREDICTION")
    print("==================================================")
    print(f"Historical Average Growth:      +{avg_historical_growth:.2f} points")
    print(f"Current 2026-2027 Fall Average: {current_year['Fall_Avg'].values[0]:.2f}")
    print(f"--> PREDICTED Spring Average:   {predicted_spring:.2f}")
    print("==================================================\n")

    # Generate the bar chart
    plt.figure(figsize=(10, 6))
    x = np.arange(len(df))
    width = 0.35

    # Plot Fall Averages
    plt.bar(x - width/2, df['Fall_Avg'], width, label='Fall Average', color='#1f77b4')
    
    # Plot Historical Spring Averages
    plt.bar(history.index + width/2, history['Spring_Avg'], width, label='Spring Average (Actual)', color='#2ca02c')
    
    # Plot Predicted Spring 2027 Average
    plt.bar(current_year.index + width/2, [predicted_spring], width, 
            label='Spring Average (Predicted)', color='#ff7f0e', hatch='//', alpha=0.8)

    plt.title("Longitudinal Cohort Growth (2021-2027)\nPredicting Spring Outcomes", pad=15)
    plt.ylabel("Average RIT Score")
    plt.xticks(x, df['Year'])
    plt.ylim(220, 260)  # Zooms in on the relevant score range to make differences visible
    
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Saved visualization to: {output_path.name}")


def main():
    # Setup paths relative to this script
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    output_dir = project_root / "docs" / "images"

    # Run the pipeline
    stats_df = load_growth_data(data_dir)
    
    if not stats_df.empty:
        analyze_and_plot(stats_df, output_dir / "longitudinal_growth_prediction.png")
    else:
        print("No data found to process. Please check your data folder.")


if __name__ == "__main__":
    main()