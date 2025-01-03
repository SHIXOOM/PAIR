import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pathlib import Path
import os
from typing import List, Tuple


class VisualizationsManager:
    DATA_DIR = Path(__file__).parent.parent / "data"

    @staticmethod
    def findExperimentFiles(dataDir: str | Path) -> List[Tuple[Path, Path]]:
        """Find all iteration CSV files and generate their save paths"""
        results = []
        data_path = Path(dataDir).resolve()  # Get absolute path

        if not data_path.exists():
            raise FileNotFoundError(f"Data directory not found: {data_path}")

        for problem_dir in data_path.glob("*"):
            if problem_dir.is_dir():
                for csv_file in problem_dir.glob("*_iterations.csv"):
                    # Create visualization subdirectory for this problem
                    vis_dir = problem_dir / "visualizations"
                    vis_dir.mkdir(parents=True, exist_ok=True)

                    # Return Path objects instead of strings
                    results.append((csv_file, vis_dir))

        return results

    @staticmethod
    def generateSavePath(visDir: str | Path, expId: str, plotType: str) -> Path:
        """Generate save path for a visualization"""
        return Path(visDir) / f"{expId}_{plotType}.svg"

    @staticmethod
    def visualizeAllExperiments(dataDir: str | Path = None):
        """Process all experiments in the data directory"""
        # Use default DATA_DIR if no directory is specified
        data_dir = Path(dataDir) if dataDir else VisualizationsManager.DATA_DIR
        
        try:
            experiment_files = VisualizationsManager.findExperimentFiles(data_dir)
            
            if not experiment_files:
                print(f"No experiment files found in {data_dir}")
                return

            for csv_path, vis_dir in experiment_files:
                try:
                    # Extract experiment ID from the CSV filename
                    exp_id = csv_path.stem.replace('_iterations', '')

                    # Generate save paths for each plot type
                    gap_save_path = VisualizationsManager.generateSavePath(vis_dir, exp_id, "gap")
                    var_save_path = VisualizationsManager.generateSavePath(vis_dir, exp_id, "variance")
                    temp_save_path = VisualizationsManager.generateSavePath(vis_dir, exp_id, "temperature")
                    var_temp_save_path = VisualizationsManager.generateSavePath(vis_dir, exp_id, "variance_temperature")

                    # Generate all visualizations with str paths
                    VisualizationsManager.plotOptimalityGapConvergence(str(csv_path), str(gap_save_path))
                    VisualizationsManager.plotVariance(str(csv_path), str(var_save_path))
                    VisualizationsManager.plotAdaptiveTemperature(str(csv_path), str(temp_save_path))
                    VisualizationsManager.plotVarianceTemperature(str(csv_path), str(var_temp_save_path))

                    print(f"Successfully processed experiment: {exp_id}")

                except Exception as e:
                    print(f"Error processing {csv_path}: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error accessing data directory {data_dir}: {str(e)}")

    @staticmethod
    def plotOptimalityGapConvergence(loadPath: str, savePath: str):
        data = VisualizationsManager.loadData(loadPath)

        with plt.style.context('seaborn-v0_8-paper'):
            fig, ax = plt.subplots(figsize=(12, 7))

            # Main line plot
            sns.lineplot(data=data,
                         x='iteration',
                         y='gap',
                         color='#34495e',
                         linewidth=2,
                         errorbar=None)

            # Add points with variance-based color gradient
            scatter = ax.scatter(data['iteration'],
                                 data['gap'],
                                 c=data['variance'],  # Color based on variance
                                 cmap='RdYlBu_r',  # Red (high variance) to Blue (low variance)
                                 s=50,
                                 alpha=0.8)

            # Add trend line
            z = np.polyfit(data['iteration'], data['gap'], 3)
            p = np.poly1d(z)
            plt.plot(data['iteration'],
                     p(data['iteration']),
                     "r--",
                     alpha=0.8,
                     label='Trend')

            # Styling
            plt.title('Optimality Gap with Population Diversity Across Generations',
                      fontsize=16,
                      pad=20)
            plt.xlabel('Generation', fontsize=12)
            plt.ylabel('Optimality Gap (%)', fontsize=12)

            # Add colorbar showing variance scale
            cbar = plt.colorbar(scatter)
            cbar.set_label('Population Variance ($σ^2$)', fontsize=10)

            # Legend
            plt.legend(['Gap Trajectory', 'Solution Points', 'Trend Line'])

            # Grid
            plt.grid(True, linestyle='--', alpha=0.3)

            # Clean spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Add annotations for key points
            initial_gap = data['gap'].iloc[0]
            final_gap = data['gap'].iloc[-1]

            plt.annotate(f'Initial Gap: {initial_gap:.1f}%',
                         xy=(data['iteration'].iloc[0], initial_gap),
                         xytext=(10, 10),
                         textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.5',
                                   fc='white',
                                   ec='gray',
                                   alpha=0.9))

            plt.annotate(f'Final Gap: {final_gap:.1f}%',
                         xy=(data['iteration'].iloc[-1], final_gap),
                         xytext=(-60, 10),
                         textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.5',
                                   fc='white',
                                   ec='gray',
                                   alpha=0.9))

            plt.tight_layout()

            # Save with high quality
            # savePath (example)= 'Optimality_Gap_Convergence_Plot_Rue_10_3.svg'
            plt.savefig(savePath,
                        format='svg',
                        dpi=300,
                        bbox_inches='tight')

    @staticmethod
    def plotVariance(loadPath: str, savePath: str):
        data = VisualizationsManager.loadData(loadPath)

        # Variance vs Generations

        # Set style for academic visualization
        plt.style.use('seaborn-v0_8-paper')
        sns.set_context("paper", font_scale=1.2)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create gradient color fill based on variance values
        norm = plt.Normalize(data['variance'].min(), data['variance'].max())
        colors = plt.cm.RdYlBu_r(norm(data['variance']))  # Higher variance = warmer colors

        # Fill between with variance-based colors
        for i in range(len(data['iteration']) - 1):
            plt.fill_between(data['iteration'][i:i + 2],
                             data['variance'][i:i + 2],
                             color=colors[i],
                             alpha=0.4)

        # Add line plot
        plt.plot(data['iteration'],
                 data['variance'],
                 color='#2f4858',
                 linewidth=1.2,
                 alpha=0.7)

        # Academic styling
        plt.title('Population Diversity Analysis\nTour Length Variance Distribution',
                  fontsize=14,
                  pad=20,
                  fontweight='medium')
        plt.xlabel('Generation Number', fontsize=12, labelpad=10)
        plt.ylabel('Tour Length Variance', fontsize=12, labelpad=10)

        # Refined grid
        plt.grid(True, linestyle=':', alpha=0.3, color='gray')

        # Clean spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)

        # Add annotations
        max_variance = data['variance'].max()
        final_variance = data['variance'].iloc[-1]

        plt.annotate(f'Maximum Diversity\n$σ^2={max_variance:.1f}$',
                     xy=(data['iteration'][data['variance'].idxmax()], max_variance),
                     xytext=(10, 20),
                     textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.5',
                               fc='white',
                               ec='gray',
                               alpha=0.9,
                               linewidth=0.5),
                     arrowprops=dict(arrowstyle='->',
                                     connectionstyle='arc3,rad=0.2',
                                     linewidth=0.5))

        plt.annotate(f'Final Diversity\n$σ^2={final_variance:.1f}$',
                     xy=(data['iteration'].iloc[-1], final_variance),
                     xytext=(-60, 20),
                     textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.5',
                               fc='white',
                               ec='gray',
                               alpha=0.9,
                               linewidth=0.5),
                     arrowprops=dict(arrowstyle='->',
                                     connectionstyle='arc3,rad=-0.2',
                                     linewidth=0.5))

        # Add colorbar showing variance scale
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=norm)
        sm.set_array([])
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.15)
        cbar = plt.colorbar(sm, cax=cax)
        cbar.set_label('Variance Magnitude', fontsize=10)
        cbar.ax.tick_params(labelsize=9)

        # Set y-axis to start from 0
        plt.margins(x=0.02)
        plt.ylim(bottom=0)

        plt.tight_layout()

        # Save with high quality
        # savePath (example)= 'Variance_Plot_Rue_10_3.svg'
        plt.savefig(savePath,
                    format='svg',
                    dpi=300,
                    bbox_inches='tight',
                    metadata={'Creator': 'Matplotlib'})

    @staticmethod
    def plotAdaptiveTemperature(loadPath: str, savePath: str):
        data = VisualizationsManager.loadData(loadPath)

        # Temperature vs Generations

        # Set style for academic visualization
        plt.style.use('seaborn-v0_8-paper')
        sns.set_context("paper", font_scale=1.2)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create gradient color fill based on temperature values
        norm = plt.Normalize(data['temperature'].min(), data['temperature'].max())
        colors = plt.cm.RdYlBu_r(norm(data['temperature']))  # Higher temperature = warmer colors

        # Plot temperature evolution with color gradient
        for i in range(len(data['iteration']) - 1):
            plt.plot(data['iteration'][i:i + 2],
                     data['temperature'][i:i + 2],
                     color=colors[i],
                     linewidth=2.5)

        # Academic styling
        plt.title('Adaptive Temperature\nDynamic Temperature Control Across Generations',
                  fontsize=14,
                  pad=20,
                  fontweight='medium')
        plt.xlabel('Generation', fontsize=12, labelpad=10)
        plt.ylabel('LLM\'s Temperature ($τ$)', fontsize=12, labelpad=10)  # Using LaTeX notation

        # Refined grid
        plt.grid(True, linestyle=':', alpha=0.3, color='gray')

        # Clean spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)

        # Add annotations for key points
        initial_temp = data['temperature'].iloc[0]
        final_temp = data['temperature'].iloc[-1]
        max_temp = data['temperature'].max()

        plt.annotate(f'Initial Temperature\n$τ={initial_temp:.2f}$',
                     xy=(data['iteration'].iloc[0], initial_temp),
                     xytext=(10, -20),
                     textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.5',
                               fc='white',
                               ec='gray',
                               alpha=0.9,
                               linewidth=0.5),
                     arrowprops=dict(arrowstyle='->',
                                     connectionstyle='arc3,rad=0.2',
                                     linewidth=0.5))

        plt.annotate(f'Final Temperature\n$τ={final_temp:.2f}$',
                     xy=(data['iteration'].iloc[-1], final_temp),
                     xytext=(-60, 20),
                     textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.5',
                               fc='white',
                               ec='gray',
                               alpha=0.9,
                               linewidth=0.5),
                     arrowprops=dict(arrowstyle='->',
                                     connectionstyle='arc3,rad=-0.2',
                                     linewidth=0.5))

        # Add colorbar showing temperature scale
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=norm)
        sm.set_array([])
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.15)
        cbar = plt.colorbar(sm, cax=cax)
        cbar.set_label('Temperature Value ($τ$)', fontsize=10)
        cbar.ax.tick_params(labelsize=9)

        # Set y-axis limits with some padding
        plt.margins(x=0.02)
        ymin, ymax = data['temperature'].min(), data['temperature'].max()
        plt.ylim(ymin - 0.05 * (ymax - ymin), ymax + 0.05 * (ymax - ymin))

        plt.tight_layout()

        # Save with high quality
        # savePath (example)= 'Adaptive_Temperature_Plot_Rue_10_3.svg'
        plt.savefig(savePath,
                    format='svg',
                    dpi=300,
                    bbox_inches='tight',
                    metadata={'Creator': 'Matplotlib'})

    @staticmethod
    def plotVarianceTemperature(loadPath: str, savePath: str):
        data = VisualizationsManager.loadData(loadPath)

        # Create figure and axis
        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        # Create box plot
        # Group data by temperature and create list of variance values for each temperature
        temp_groups = data.groupby('temperature')['variance'].apply(list).values
        positions = np.arange(len(data['temperature'].unique())) * 2  # Multiply by 2 to stretch out positions
        temp_values = sorted(data['temperature'].unique())

        # Create box plot with wider boxes and custom style
        bp = plt.boxplot(temp_groups,
                         positions=positions,
                         patch_artist=True,
                         widths=0.8,  # Wider boxes
                         medianprops=dict(color="black", linewidth=1.5),
                         flierprops=dict(marker='o', markerfacecolor='gray', markersize=8, alpha=0.5),
                         whiskerprops=dict(linewidth=1.5),
                         capprops=dict(linewidth=1.5))

        # Set consistent color for all boxes
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)
            patch.set_edgecolor('black')
            patch.set_linewidth(1.5)

        # Set x-ticks to show actual temperature values
        plt.xticks(positions, [f'{temp:.2f}' for temp in temp_values], rotation=45)

        # Add labels and title with enhanced styling
        plt.xlabel('LLM\'s Temperature ($τ$)', fontsize=12, labelpad=10)
        plt.ylabel('Population Variance', fontsize=12, labelpad=10)
        plt.title('Distribution of Population Variance at Different Temperatures',
                  fontsize=14, pad=20)

        # Add grid with enhanced styling
        plt.grid(True, linestyle='--', alpha=0.5, axis='y', which='major')

        # Set axis limits with some padding
        ymin, ymax = data['variance'].min(), data['variance'].max()
        padding = 0.1 * (ymax - ymin)
        plt.ylim(ymin - padding, ymax + padding)

        # Set x-axis limits to show full boxes with padding
        plt.xlim(min(positions) - 1.5, max(positions) + 1.5)

        plt.tight_layout()

        # Save with high quality
        # savePath (example)= 'Variance_Temperature_Plot_Rue_10_3.svg'
        plt.savefig(savePath,
                    format='svg',
                    dpi=300,
                    bbox_inches='tight',
                    metadata={'Creator': 'Matplotlib'})

    # private methods
    @staticmethod
    def loadData(dataPath: str) -> pd.DataFrame:
        data = pd.read_csv(dataPath)
        data = data.drop(labels=data.columns[0], axis=1)
        return data


if __name__ == "__main__":
    VisualizationsManager.visualizeAllExperiments()