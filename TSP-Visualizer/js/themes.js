export const themes = {
	blue: {
		node: "#007bff",
		bestPath: "#ff4444",
		paths: [
			// "#F8FBFF",
			// "#E3F2FD",
			// "#BBDEFB",
			// "#90CAF9",
			"#64B5F6",
			// "#42A5F5",
			// "#2196F3",
			// "#1E88E5",
			// "#1976D2",
			// "#1565C0",
			// "#0D47A1",
			// "#0A3A82",
			// "#072D64",
			// "#052046",
			// "#031328",
			// "#01060A",
		],
		panel: "#007bff",
	},
	red: {
		node: "#dc3545",
		bestPath: "#007bff",
		paths: [
			// "#FFF5F5",
			// "#FFE3E3",
			// "#FFC9C9",
			// "#FFA8A8",
			// "#FF8787",
			// "#FF6B6B",
			// "#FA5252",
			"#F03E3E",
			// "#E03131",
			// "#C92A2A",
			// "#B02525",
			// "#962020",
			// "#7D1A1A",
			// "#641515",
			// "#4A1010",
			// "#310B0B",
		],
		panel: "#dc3545",
	},
	dark: {
		node: "#2c3e50",
		bestPath: "#e74c3c",
		paths: [
			// "#F8F9FA",
			// "#E9ECEF",
			// "#DEE2E6",
			// "#CED4DA",
			// "#ADB5BD",
			// "#868E96",
			// "#6C757D",
			// "#495057",
			"#343A40",
			// "#212529",
			// "#1A1E21",
			// "#141619",
			// "#0D0F10",
			// "#070808",
			// "#030404",
			// "#000000",
		],
		panel: "#3498db",
	},
};

export class ThemeManager {
	constructor() {
		this.currentTheme = "blue";
		this.initializeThemeSelectors();
	}

	initializeThemeSelectors() {
		document.querySelectorAll(".theme-circle").forEach((circle) => {
			circle.addEventListener("click", (e) => this.handleThemeChange(e));
		});
		this.updateUIColors();
	}

	handleThemeChange(e) {
		const prevTheme = this.currentTheme;
		this.currentTheme = e.target.dataset.theme;

		document
			.querySelector(`.theme-circle[data-theme="${prevTheme}"]`)
			.classList.remove("active");
		e.target.classList.add("active");

		this.updateUIColors();
	}

	updateUIColors() {
		document.querySelectorAll("button").forEach((btn) => {
			btn.style.backgroundColor = themes[this.currentTheme].node;
		});
		document.querySelector(".speed-control label").style.color =
			themes[this.currentTheme].panel;
	}

	getCurrentTheme() {
		return themes[this.currentTheme];
	}

	getPathColor(index) {
		const currentTheme = this.getCurrentTheme();
		return currentTheme.paths[index % currentTheme.paths.length];
	}
}
