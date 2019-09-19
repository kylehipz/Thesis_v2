var $ = jQuery.noConflict();

$(document).ready(function() {
	$('#homeowners_table').DataTable();
});

$(document).ready(function() {
	$('#admins_table').DataTable();
});

$(document).ready(function() {
	$("#hidden_button").click(() => {
		$.ajax({
			type: "GET",
			url: "/get_logs",
			mimeType: "json",
			success: function(data) {
				$("#logs_table tbody").html("");

				$.each(data, function(i, data) {
					$("#logs_table tbody").append(`
						<tr>
							<td>${data.plate_number}</td>
							<td>${data.visitor}</td>
							<td>${data.owner}</td>
							<td>${data.status}</td>
							<td>${data.date}</td>
						</tr>`)
				});
				$("#logs_table").DataTable();
			}
		});
	})

	setInterval(() => {
		$('#hidden_button').click();
	}, 2000)

});
