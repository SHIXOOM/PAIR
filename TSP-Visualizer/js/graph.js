export class GraphVisualizer {
	constructor(canvas, themeManager, numNodes) {
		this.canvas = canvas;
		this.ctx = canvas.getContext("2d");
		this.themeManager = themeManager;
		this.numNodes = numNodes;
		this.currentPath = [];
		this.bestPath = [];
		this.resize();
	}

	calculateNodePositions(centerX, centerY, radius) {
		const positions = [];
		for (let i = 0; i < this.numNodes; i++) {
			const angle = (i * 2 * Math.PI) / this.numNodes - Math.PI / 2;
			positions.push({
				id: i + 1,
				x: centerX + radius * Math.cos(angle),
				y: centerY + radius * Math.sin(angle),
			});
		}
		return positions;
	}

	resize() {
		if (!this.canvas) return;

		this.canvas.width = this.canvas.parentElement.clientWidth - 240;
		this.canvas.height = window.innerHeight - 40;

		// shift center right to account for left panel
		const centerX = this.canvas.width / 2 + 140;
		const centerY = this.canvas.height / 2;
		const radius = Math.min(centerX - 300, centerY - 100);

		this.nodes = this.calculateNodePositions(centerX, centerY, radius);
		this.draw();
	}

	drawGrid() {
		const gridSize = 50;
		const theme = this.themeManager.getCurrentTheme();

		// grid lines color and width
		this.ctx.strokeStyle = "rgba(200, 200, 200, 0.6)";
		this.ctx.lineWidth = 0.5;

		// draw vertical lines
		for (let x = gridSize; x < this.canvas.width; x += gridSize) {
			this.ctx.beginPath();
			this.ctx.moveTo(x, 0);
			this.ctx.lineTo(x, this.canvas.height);
			this.ctx.stroke();
		}

		// draw horizontal lines
		for (let y = gridSize; y < this.canvas.height; y += gridSize) {
			this.ctx.beginPath();
			this.ctx.moveTo(0, y);
			this.ctx.lineTo(this.canvas.width, y);
			this.ctx.stroke();
		}

		// reset line settings
		this.ctx.lineWidth = 1;
		this.ctx.strokeStyle = theme.node;
	}

	drawNode(node) {
		const theme = this.themeManager.getCurrentTheme();

		// Node glow effect
		const gradient = this.ctx.createRadialGradient(node.x, node.y, 5, node.x, node.y, 15);
		gradient.addColorStop(0, theme.node);
		gradient.addColorStop(1, "rgba(0,0,0,0)");

		this.ctx.beginPath();
		this.ctx.arc(node.x, node.y, 25, 0, Math.PI * 2);
		this.ctx.fillStyle = gradient;
		this.ctx.fill();

		// Main node
		this.ctx.beginPath();
		this.ctx.arc(node.x, node.y, 15, 0, Math.PI * 2);
		this.ctx.fillStyle = theme.node;
		this.ctx.fill();

		// Node border
		this.ctx.strokeStyle = "#282828";
		this.ctx.lineWidth = 2;
		this.ctx.stroke();

		// Node label
		this.ctx.fillStyle = "white";
		this.ctx.font = "bold 12px Arial";
		this.ctx.textAlign = "center";
		this.ctx.textBaseline = "middle";
		this.ctx.fillText(node.id, node.x, node.y);
	}

	drawPath(path, isCurrentPath = true) {
		if (path.length < 2) return;

		const theme = this.themeManager.getCurrentTheme();
		this.ctx.beginPath();

		// Ensure path indices are valid
		if (!this.nodes[path[0]]) {
			console.error(`Invalid path index: ${path[0]}`);
			return;
		}

		this.ctx.moveTo(this.nodes[path[0]].x, this.nodes[path[0]].y);

		for (let i = 1; i < path.length; i++) {
			if (!this.nodes[path[i]]) {
				console.error(`Invalid path index: ${path[i]}`);
				return;
			}
			this.ctx.lineTo(this.nodes[path[i]].x, this.nodes[path[i]].y);
		}

		// Complete the cycle
		if (!this.nodes[path[0]]) {
			console.error(`Invalid path index: ${path[0]}`);
			return;
		}
		this.ctx.lineTo(this.nodes[path[0]].x, this.nodes[path[0]].y);

		if (isCurrentPath) {
			this.ctx.strokeStyle = this.themeManager.getPathColor(path[0]);
			this.ctx.lineWidth = 2;
		} else {
			this.ctx.strokeStyle = theme.bestPath;
			this.ctx.lineWidth = 1;
			this.ctx.setLineDash([5, 5]);
		}

		this.ctx.stroke();
		this.ctx.setLineDash([]);
	}

	updatePaths(currentPath, bestPath) {
		this.currentPath = currentPath;
		this.bestPath = bestPath;
		this.draw();
	}

	draw() {
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

		// Draw background grid
		this.drawGrid();

		// Draw paths
		if (this.bestPath.length > 0) {
			this.drawPath(this.bestPath, false);
		}
		if (this.currentPath.length > 0) {
			this.drawPath(this.currentPath, true);
		}

		// Draw nodes on top
		this.nodes.forEach((node) => this.drawNode(node));
	}
}
