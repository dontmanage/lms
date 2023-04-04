dontmanage.ready(function () {
	dontmanage.web_form.after_save = () => {
		let data = dontmanage.web_form.get_values();
		if (data.class) {
			setTimeout(() => {
				window.location.href = `/classes/${data.class}`;
			}, 2000);
		}
	};
});
