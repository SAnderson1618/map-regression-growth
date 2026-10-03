"""MAP Score Longitudinal Regression Analysis.

Loads 5 years of Fall MAP data (2022-2027), standardizes columns,
performs linear regression using SciPy, and generates regression plots.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns


def load_and_standardize_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load MAP spreadsheets and standardize differing column names."""
    files = {
        "2022-2023": data_dir / "2022_2023 MAP Data.xlsx",
        "2023-2024": data_dir / "2023_2024 MAP Data.xlsx",
        "2024-2025": data_dir / "2024_2025 MAP Data.xlsx",
        "2025-2026": data_dir / "2025_2026 MAP Data.xlsx",
        "2026-2027": data_dir / "2026_2027 MAP Data.xlsx",
    }

    dfs = {}
    for year, file_path in files.items():
        if not file_path.exists():
            print(f"Warning: {file_path.name} not found.")
            continue

        df = pd.read_excel(file_path)

        # Standardize subject column
        if "Unnamed: 0" in df.columns:
            df = df.rename(columns={"Unnamed: 0": "Subject"})

        # Standardize RIT score column
        if "Rit Score" in df.columns:
            df = df.rename(columns={"Rit Score": "RitScore"})

        # Standardize duration column
        if "Duration in minutes" in df.columns:
            df = df.rename(columns={"Duration in minutes": "Duration"})

        # Standardize percentile column
        if "AchievementPercentile" in df.columns:
            df = df.rename(columns={"AchievementPercentile": "Achievement Percentile"})

        dfs[year] = df
        print(f"Loaded {year}: {len(df)} rows.")

    return dfs


def run_regression(
    df: pd.DataFrame, x_col: str, y_col: str, title: str, output_path: Path
) -> stats._stats_mstats_common.LinregressResult:
    """Run linear regression between two variables and save a scatter plot with fit line."""
    clean = df[[x_col, y_col]].dropna()
    x = clean[x_col]
    y = clean[y_col]

    result = stats.linregress(x, y)

    print(f"\n==================================================")
    print(f"  Linear Regression: {title}")
    print(f"==================================================")
    print(f"  Sample Size (N): {len(clean)}")
    print(f"  Slope:           {result.slope:.4f}")
    print(f"  Intercept:       {result.intercept:.4f}")
    print(f"  R-value (r):     {result.rvalue:.4f}")
    print(f"  R-squared (R²):  {result.rvalue**2:.4f}")
    print(f"  P-value:         {result.pvalue:.4e}")
    print(f"  Standard Error:  {result.stderr:.4f}")
    print(f"  Linear Equation: y = {result.slope:.2f}x + {result.intercept:.2f}")

    # Plot
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        x=x, y=y, alpha=0.75, color="#1f77b4", edgecolor="none", s=50, label="Observed Students"
    )

    reg_line = result.intercept + result.slope * x
    plt.plot(
        x,
        reg_line,
        color="#d62728",
        linewidth=2,
        label=f"Fit: y = {result.slope:.2f}x + {result.intercept:.2f}\n(R² = {result.rvalue**2:.3f})",
    )

    plt.title(f"{title}\n(N={len(clean)}, p < 0.001)", fontsize=12, pad=10)
    plt.xlabel(x_col, fontsize=10)
    plt.ylabel(y_col, fontsize=10)
    plt.legend(frameon=True)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"  --> Saved plot: {output_path.name}")

    return result


def main() -> None:
    """Run data loading and regression analyses."""
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    output_dir = project_root / "docs" / "images"

    datasets = load_and_standardize_data(data_dir)

    # 1. 2026-2027: Algebra and Functions vs Overall RitScore
    if "2026-2027" in datasets:
        df_26 = datasets["2026-2027"]
        run_regression(
            df_26,
            x_col="Algebra and Functions",
            y_col="RitScore",
            title="2026-2027 Fall MAP: Algebra & Functions vs Overall RIT",
            output_path=output_dir / "regression_algebra_vs_rit_2026.png",
        )

        # 2. 2026-2027: Geometry Subscore vs Overall RitScore
        run_regression(
            df_26,
            x_col="Geometry",
            y_col="RitScore",
            title="2026-2027 Fall MAP: Geometry Subscore vs Overall RIT",
            output_path=output_dir / "regression_geometry_vs_rit_2026.png",
        )

        # 3. 2026-2027: Duration vs Overall RitScore
        run_regression(
            df_26,
            x_col="Duration",
            y_col="RitScore",
            title="2026-2027 Fall MAP: Test Duration vs Overall RIT",
            output_path=output_dir / "regression_duration_vs_rit_2026.png",
        )

    print("\nAll regression analyses completed successfully!")


if __name__ == "__main__":
    main()