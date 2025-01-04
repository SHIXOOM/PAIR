export class Animator {
	constructor(graph, infoPanel, dataManager) {
		this.graph = graph;
		this.infoPanel = infoPanel;
		this.dataManager = dataManager;
		this.isPaused = false;
		this.animationSpeed = 200;
		this.currentStep = 0;
		this.currentGeneration = 0;
		this.animationFrameId = null;
	}

	setSpeed(sliderValue) {
		this.animationSpeed = Math.max(5, 500 * Math.pow(0.95, parseInt(sliderValue)));
	}

	togglePause() {
		this.isPaused = !this.isPaused;
		if (!this.isPaused) {
			this.animate(this.currentGeneration);
		}
		return this.isPaused;
	}

	animate(generationIndex) {
		if (this.isPaused) {
			this.animationFrameId = requestAnimationFrame(() => this.animate(generationIndex));
			return;
		}

		const currentData = this.dataManager.getCurrentGeneration(generationIndex);
		if (!currentData) {
			cancelAnimationFrame(this.animationFrameId);
			return;
		}

		const population = currentData.population;
		if (this.currentStep >= population.length) {
			this.currentStep = 0;
			this.currentGeneration++;
			setTimeout(() => this.animate(this.currentGeneration), this.animationSpeed);
			return;
		}

		const currentPopMember = population[this.currentStep];
		const currentPath = currentPopMember[0].map((x) => x - 1);
		const currentSolution = currentPopMember[1];

		// update best solution before drawing
		this.dataManager.checkAndUpdateBestSolution(currentSolution, currentPopMember[0]);

		this.graph.updatePaths(currentPath, this.dataManager.bestPathEver);
		this.infoPanel.draw(
			currentData,
			this.currentStep,
			this.dataManager.bestSolutionEver,
			this.currentGeneration,
			this.dataManager.totalGenerations,
			this.dataManager.generationsData
		);

		this.currentStep++;
		setTimeout(() => {
			this.animationFrameId = requestAnimationFrame(() => this.animate(generationIndex));
		}, this.animationSpeed);
	}
}
