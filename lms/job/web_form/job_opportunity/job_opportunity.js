dontmanage.ready(function () {
	dontmanage.web_form.after_save = () => {
		setTimeout(() => {
			window.location.href = `/jobs`;
		});
	};
});
