const { defineConfig } = require("cypress");

module.exports = defineConfig({
	projectId: "vandxn",
	adminPassword: "admin",
	testUser: "dontmanage@example.com",
	defaultCommandTimeout: 20000,
	pageLoadTimeout: 15000,
	video: true,
	videoUploadOnPasses: false,
	retries: {
		runMode: 2,
		openMode: 0,
	},
	e2e: {
		baseUrl: "http://test_site_ui:8000",
	},
});