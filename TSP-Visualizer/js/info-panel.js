export class InfoPanel {
	constructor(ctx, themeManager) {
		this.ctx = ctx;
		this.themeManager = themeManager;
	}

	draw(
		generationData,
		currentStep,
		bestSolution,
		currentGeneration,
		totalGenerations,
		allGenerationsData
	) {
		if (!generationData) return;

		const status = generationData.status;
		const currentSolution = generationData.population[currentStep][1];

		const panelWidth = 280;
		const panelHeight = 280;
		const panelX = 20;
		const panelY = 20;

		// draw semi-transparent background
		this.ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
		this.ctx.fillRect(panelX - 5, panelY - 5, panelWidth + 10, panelHeight + 10);

		this.drawPanelBackground(panelX, panelY, panelWidth, panelHeight);

		// use theme colors for text
		const theme = this.themeManager.getCurrentTheme();
		this.ctx.fillStyle = theme.panel;

		this.drawGenerationStats(
			panelX,
			panelY,
			status,
			currentStep,
			currentSolution,
			bestSolution,
			currentGeneration,
			totalGenerations
		);

		this.drawTemperatureBar(panelX, panelY + 130, status.temperature);
		this.drawVarianceGraph(
			panelX,
			panelY + 185,
			status.variance,
			currentGeneration,
			allGenerationsData
		);
	}

	drawPanelBackground(x, y, width, height) {
		const theme = this.themeManager.getCurrentTheme();
		this.ctx.fillStyle = "rgba(255, 255, 255, 0.95)";
		this.ctx.fillRect(x, y, width, height);
		this.ctx.strokeStyle = theme.panel;
		this.ctx.lineWidth = 2;
		this.ctx.strokeRect(x, y, width, height);
	}

	drawGenerationStats(
		x,
		y,
		status,
		currentStep,
		currentSolution,
		bestSolution,
		currentGeneration,
		totalGenerations
	) {
		this.ctx.fillStyle = "black";
		this.ctx.font = "14px Arial";
		this.ctx.textAlign = "left";

		let textY = y + 25;
		const lineHeight = 22;

		// draw text info
		this.ctx.fillText(
			`Generation: ${currentGeneration + 1} / ${totalGenerations}`,
			x + 15,
			textY
		);
		textY += lineHeight;

		this.ctx.fillText(
			`Population Member: ${currentStep + 1} / ${status.population_size}`,
			x + 15,
			textY
		);
		textY += lineHeight;

		this.ctx.fillText(`Current Solution: ${currentSolution}`, x + 15, textY);
		textY += lineHeight;

		this.ctx.fillText(`Best Solution Ever: ${bestSolution}`, x + 15, textY);
	}

	drawTemperatureBar(x, y, temperature) {
		const barWidth = 250;
		const barHeight = 20;

		// temperature label
		this.ctx.fillStyle = "black";
		this.ctx.fillText(`Temperature: ${temperature}`, x + 15, y - 8);

		// bar background
		this.ctx.fillStyle = "#f0f0f0";
		this.ctx.fillRect(x + 15, y + 5, barWidth, barHeight);

		// temperature bar fill
		const normalizedTemp = (temperature - 1) / 0.5;
		const tempColor = `hsl(${Math.max(0, (1 - normalizedTemp) * 120)}, 100%, 50%)`;
		this.ctx.fillStyle = tempColor;
		this.ctx.fillRect(x + 15, y + 5, barWidth * normalizedTemp, barHeight);
	}

	drawVarianceGraph(x, y, variance, currentGeneration, generationsData) {
		const graphWidth = 250;
		const graphHeight = 40;
		const maxVariance = 1500;
		const theme = this.themeManager.getCurrentTheme();

		// variance label
		this.ctx.fillStyle = "black";
		this.ctx.fillText(`Population Variance: ${variance.toFixed(2)}`, x + 15, y - 8);

		// background
		this.ctx.fillStyle = "#f0f0f0";
		this.ctx.fillRect(x + 15, y + 5, graphWidth, graphHeight);

		// scale lines
		this.drawVarianceScaleLines(x + 15, y + 5, graphWidth, graphHeight, maxVariance);

		// get last 10 generations variance history
		const varHistory = [];
		const startGen = Math.max(0, currentGeneration - 10);
		for (let i = startGen; i <= currentGeneration; i++) {
			if (generationsData && generationsData[i]) {
				varHistory.push(generationsData[i].status.variance);
			}
		}

		// only draw if we have data
		if (varHistory.length > 0) {
			// plot variance line
			this.ctx.beginPath();
			const varStep = graphWidth / (varHistory.length - 1 || 1);
			varHistory.forEach((var_value, i) => {
				const plotX = x + 15 + i * varStep;
				const plotY =
					y +
					5 +
					graphHeight -
					(Math.min(var_value, maxVariance) / maxVariance) * graphHeight;

				if (i === 0) {
					this.ctx.moveTo(plotX, plotY);
				} else {
					this.ctx.lineTo(plotX, plotY);
				}
			});

			// draw line
			this.ctx.strokeStyle = theme.panel;
			this.ctx.lineWidth = 2;
			this.ctx.stroke();

			// draw points
			varHistory.forEach((var_value, i) => {
				const plotX = x + 15 + i * varStep;
				const plotY =
					y +
					5 +
					graphHeight -
					(Math.min(var_value, maxVariance) / maxVariance) * graphHeight;

				this.ctx.beginPath();
				this.ctx.arc(plotX, plotY, 3, 0, Math.PI * 2);
				this.ctx.fillStyle = theme.panel;
				this.ctx.fill();
			});
		}
	}

	drawVarianceScaleLines(x, y, width, height, maxVariance) {
		const scaleLines = [0, 500, 1000, 1500];

		this.ctx.strokeStyle = "#ddd";
		this.ctx.setLineDash([2, 2]);

		scaleLines.forEach((value) => {
			const lineY = y + height - (value / maxVariance) * height;

			this.ctx.beginPath();
			this.ctx.moveTo(x, lineY);
			this.ctx.lineTo(x + width, lineY);
			this.ctx.stroke();

			// scale labels
			this.ctx.fillStyle = "#666";
			this.ctx.font = "10px Arial";
			this.ctx.fillText(value.toString(), x + 5, lineY + 3);
		});

		this.ctx.setLineDash([]);
	}
}
