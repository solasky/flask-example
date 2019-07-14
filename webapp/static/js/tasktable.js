$(document).ready(function() {
	var table = $('#tasktable').DataTable({
		bProcessing: true,
		bServerSide: true,
		sPaginationType: "full_numbers",
	    lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
	    iDisplayLength: 25,
	    bjQueryUI: true,
	    sAjaxSource: "/tasks/",
	    sScrollY: "auto",
	    sScrollX: "100%",
	    sScrollXInner: "100%",
//	    fnDrawCallback: function( settings ) {
//	        $(".paginate_button").removeClass("disabled");
//	    },
	    columnDefs: [
	    	{"targets": [8, 9,10,11,12,13], "render": function(timestamp) {
	    		if(timestamp == null) return '';
	    		else {
	    			return new Date(timestamp*1000).toISOString();
	    		}
	    	}},
	    	{"targets": [15,19,20], "visible": false}
	    ],
	    aoColumns: [
	    	{"class": "details-control", "mData": null, "sDefaultContent": "", "bSortable": false},
	    	{"mData": "index"},
			{"mData": "object_id"},
			{"mData": "task_status", "sDefaultContent": "", "sWidth": "10px"},
			{"mData": "n_failed", "sDefaultContent": ""},
			{"mData": "max_retries", "sDefaultContent": ""},
			{"mData": "max_timeout", "sDefaultContent": ""},
			{"mData": "priority_factor", "sDefaultContent": ""},
			{"mData": "updated_at", "sDefaultContent": ""},
			{"mData": "created_at", "sDefaultContent": ""},
			{"mData": "last_submitted", "sDefaultContent": ""},
			{"mData": "last_queried", "sDefaultContent": ""},
			{"mData": "last_success", "sDefaultContent": ""},
			{"mData": "last_failure", "sDefaultContent": ""},
			{"mData": "endpoint", "sDefaultContent": "", "bSortable": false},
			{"mData": "params", "sDefaultContent": "", "bSortable": false},
			{"mData": "task_id", "sDefaultContent": ""},
			{"mData": "state", "sDefaultContent": ""},
			{"mData": "res_status", "sDefaultContent": ""},
			{"mData": "res_data", "sDefaultContent": "", "bSortable": false},
			{"mData": "res_error", "sDefaultContent": "", "bSortable": false},
			{"mData": "f_no_total_clicks", "sDefaultContent": ""},
			{"mData": "f_no_unique_clicks", "sDefaultContent": ""},
			{"mData": "_uuid"}
	    ]
	});
	
	// To format data details
	function format(d) {
		var p = "<strong>Parameters:</strong> " + d.params;
		var res = "<strong>Response Data:</strong> " + d.res_data;
		var err = "<strong>Response Error:</strong> " + d.res_error;
		
		var text = '<div class="row-details">' + p + '</div><br>' + 
		'<div class="row-details">' + res + '</div><br>' + '<div class="row-details">' + err + '</div>';
		
		return text
	}
	
	// Add event listener for opening and closing details
    $('#tasktable').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
} );