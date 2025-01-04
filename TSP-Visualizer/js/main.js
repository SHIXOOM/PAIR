import { ThemeManager } from "./themes.js";
import { GraphVisualizer } from "./graph.js";
import { InfoPanel } from "./info-panel.js";
import { Animator } from "./animator.js";
import { DataManager } from "./data-manager.js";

class TSPVisualizer {
	constructor() {
		this.themeManager = new ThemeManager();
		this.dataManager = new DataManager();

		// Initialize these later after data is loaded
		this.graph = null;
		this.infoPanel = null;
		this.animator = null;

		this.initializeEventListeners();
	}

	initializeEventListeners() {
		window.addEventListener("resize", () => {
			if (this.graph) {
				this.graph.resize();
			}
		});

		document.getElementById("speedSlider").addEventListener("input", (e) => {
			if (this.animator) {
				this.animator.setSpeed(e.target.value);
			}
		});

		document
			.getElementById("startPauseBtn")
			.addEventListener("click", () => this.handleStartPause());
	}

	async handleStartPause() {
		if (this.dataManager.generationsData.length === 0) {
			let fileName = prompt(
				"Enter the JSON data file name (without extension):\n Leave empty for default experiment data"
			);
			if (!fileName) {
				fileName = "clu_20_1";
			}

			await this.dataManager.loadData(`parsed-data/${fileName}.json`);

			// Initialize graph, infoPanel, and animator with the number of nodes
			this.graph = new GraphVisualizer(
				document.getElementById("tspCanvas"),
				this.themeManager,
				this.dataManager.numNodes
			);
			this.infoPanel = new InfoPanel(this.graph.ctx, this.themeManager);
			this.animator = new Animator(this.graph, this.infoPanel, this.dataManager);

			document.getElementById("startPauseBtn").textContent = "Pause";
			this.graph.draw();
			this.animator.animate(0);
		} else {
			const isPaused = this.animator.togglePause();
			document.getElementById("startPauseBtn").textContent = isPaused ? "Resume" : "Pause";
		}
	}
}

// Initialize application
window.addEventListener("load", () => {
	new TSPVisualizer();
});
