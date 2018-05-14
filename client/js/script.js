$( "#searchform" ).submit(function( event ) {
	event.preventDefault();
	let url = "http://localhost:4000/?q=5";
	var jqxhr = $.getJSON( url , function(data) {
		console.log( data );
	})
		.done(function() {
			console.log( "Got results" );
		})
		.fail(function() {
			console.log( "Error" );
		})
		.always(function() {
			//var spinner = document.createElement("i");
			//<i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
		});
});

