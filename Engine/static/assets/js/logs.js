$ = jQuery.noConflict();

$(document).ready(function() {
	$.ajax({
		url: '/get_logs',
		type: 'GET',
		dataType: 'json',
		success: (logs) => {
			logs.forEach(log => {
				$('#logs_body').append(`
					<tr>
						<td>${log.plate_number}</td>
						<td>${log.visitor}</td>
						<td>${log.owner}</td>
						<td>${log.status}</td>
						<td>${log.date}</td>
					</tr>`)
			});
		}
	});
});
