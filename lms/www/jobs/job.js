dontmanage.ready(() => {
	$("#report").click((e) => {
		open_report_dialog(e);
	});

	$("#submit-report").click((e) => {
		report(e);
	});
});

const open_report_dialog = (e) => {
	e.preventDefault();
	if (dontmanage.session.user == "Guest") {
		window.location.href = `/login?redirect-to=/jobs/${$(
			e.currentTarget
		).data("job")}`;
		return;
	}
	$("#report-modal").modal("show");
};

const report = (e) => {
	dontmanage.call({
		method: "lms.job.doctype.job_opportunity.job_opportunity.report",
		args: {
			job: $(e.currentTarget).data("job"),
			reason: $(".report-field").val(),
		},
		callback: (data) => {
			$(".report-modal").modal("hide");
			dontmanage.show_alert(
				{
					message: __(
						"Thanks for informing us about this post. The admin will look into it and take an appropriate action soon."
					),
					indicator: "green",
				},
				5
			);
		},
	});
};
