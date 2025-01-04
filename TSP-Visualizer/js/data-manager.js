export class DataManager {
	constructor() {
		this.generationsData = [];
		this.bestSolutionEver = null;
		this.bestPathEver = [];
		this.totalGenerations = 0;
		this.numNodes = 0;
	}

	async loadData(filePath) {
		const response = await fetch(filePath);
		const data = await response.json();
		this.generationsData = data;
		this.totalGenerations = this.generationsData.length;
		// Extract number of nodes
		this.numNodes = this.generationsData[0].population[0][0].length;
	}

	updateBestSolution(solution, path) {
		if (solution < this.bestSolutionEver) {
			this.bestSolutionEver = solution;
			this.bestPathEver = path;
			return true;
		}
		return false;
	}

	getCurrentGeneration(index) {
		return this.generationsData[index];
	}

	checkAndUpdateBestSolution(currentSolution, currentPath) {
		if (this.bestSolutionEver === null || currentSolution < this.bestSolutionEver) {
			this.bestSolutionEver = currentSolution;
			this.bestPathEver = currentPath.map((x) => x - 1);
		}
	}
}
