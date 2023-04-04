dontmanage.ready(function () {
	dontmanage.web_form.after_save = () => {
		let data = dontmanage.web_form.get_values();
		let slug = new URLSearchParams(window.location.search).get("slug");
		dontmanage.msgprint({
			message: __("Batch {0} has been successfully created!", [
				data.title,
			]),
			clear: true,
		});
		setTimeout(function () {
			window.location.href = `courses/${slug}`;
		}, 2000);
	};

	dontmanage.web_form.validate = () => {
		let sysdefaults = dontmanage.boot.sysdefaults;
		let time_format =
			sysdefaults && sysdefaults.time_format
				? sysdefaults.time_format
				: "HH:mm:ss";
		let data = dontmanage.web_form.get_values();

		data.start_time = moment(data.start_time, time_format).format(
			time_format
		);
		data.end_time = moment(data.end_time, time_format).format(time_format);

		if (data.start_date < dontmanage.datetime.nowdate()) {
			dontmanage.msgprint(__("Start date cannot be a past date."));
			return false;
		}

		if (
			!dontmanage.datetime.validate(data.start_time) ||
			!dontmanage.datetime.validate(data.end_time)
		) {
			dontmanage.msgprint(__("Invalid Start or End Time."));
			return false;
		}

		if (data.start_time > data.end_time) {
			dontmanage.msgprint(__("Start Time should be less than End Time."));
			return false;
		}

		return true;
	};
});
