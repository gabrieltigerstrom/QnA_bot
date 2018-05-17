var currentData;
var answer_number;

function setResultData(data) {
	document.getElementById('resultTitle').innerHTML = data[0];
	document.getElementById('result').innerHTML = data[1];
}

$("#next_answer").click(function() {
	if (answer_number < currentData.length){
		answer_number++;
		setResultData(currentData[answer_number]);
		$("#previous_answer").prop('disabled', false);
		if(answer_number == currentData.length-1){
			$("#next_answer").prop('disabled', true);
		}
	}
});
$("#previous_answer").click(function() {
	if (answer_number > 0){
		answer_number--;
		setResultData(currentData[answer_number]);
		$("#next_answer").prop('disabled', false);
		if(answer_number == 0){
			$("#previous_answer").prop('disabled', true);
		}
	}
});

$( "#searchform" ).submit(function( event ) {
	event.preventDefault();
	let url = "http://localhost:4000/?q=" + $('#searchtext').val();
	var jqxhr = $.getJSON( url , function(data) {
		console.log( data );
	})
		.done(function(data) {

			console.log(data);
			currentData = data.answer;
			//TODO: Check that data contains an answer
			if(currentData.length > 0){
				setResultData(currentData[0]);
				answer_number = 0;
				$("#previous_answer").prop('hidden', false);
				$("#next_answer").prop('hidden', false);
				$("#previous_answer").prop('disabled', true);
				if(currentData.length == 1){
					$("#next_answer").prop('disabled', true);
				}
				else{
					$("#next_answer").prop('disabled', false);
				}
			} else {
				setResultData(["No results", ""]);
				answer_number = 0;
				$("#previous_answer").prop('hidden', true);
				$("#next_answer").prop('hidden', true);
				$("#previous_answer").prop('disabled', true);
				$("#next_answer").prop('disabled', true);
			}
		})
		.fail(function() {
			console.log( "Error" );
			setResultData(["Error: could not connect to server", ""]);
		})
		.always(function() {
			//var spinner = document.createElement("i");
			//<i class="fa fa-circle-o-notch fa-spin" style="font-size:24px"></i>
		});
});

