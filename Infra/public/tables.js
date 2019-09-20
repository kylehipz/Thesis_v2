var $ = jQuery.noConflict();
$(document).ready(function() {
	$("#hidden_button").click(() => {
		$.ajax({
			type: "GET",
			url: "/logs/ajax_logs",
			mimeType: "json",
			success: function(data) {
				$("#logs_table tbody").html("");

				$.each(data, function(i, data) {
					$("#logs_table tbody").append(`
						<tr>
							<td>${data.plate_number}</td>
							<td>${data.owner == 'Unknown' ? 'Yes' : 'No'}</td>
							<td>${data.owner}</td>
							<td>${data.entrance ? 'Entrance': 'Exit'}</td>
							<td>${data.date_recorded.toString()}</td>
						</tr>`)
				});
				//$("#logs_table").DataTable();
			}
		});
	})

	setInterval(() => {
		$('#hidden_button').click();
	}, 2000)

});
