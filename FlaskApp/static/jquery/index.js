
var urlUsers = "/listURL";
function initTableData() {
    $.get(urlUsers, function(responseData) {
    	var modifiedUsers = responseData.map(eachUser => {
    		return {
    			stt: eachUser.stt,
    			url: eachUser.url,
                email: eachUser.email,
  				time: eachUser.time,
  				active_key: eachUser.active_key,
  				path_img: eachUser.path_img,
    		};
    	});
        $.noConflict();
    	table = $('#urls').DataTable({
    	"processing": true,
		columnDefs: [
			{
				className: 'text-center', targets: [0, 1, 2, 3]
			}
		  ],
    	data: modifiedUsers,
    	columns:[
    		{ data: 'stt' },		
    		{ data: 'url' },
    		{ data: 'email' },
    		{ data: 'time' },
            {
                data: null,
                className: "dt-center editor-delete",
                defaultContent: '<button onclick="details();" type="button" title="Details" id="btnDetails" class="btn btn-rounded btn-outline-primary" data-toggle="modal" data-target="#ModalDetails"><i class="fa fa-eye-slash" aria-hidden="true"></i></button> <button onclick="createActiveKey();" title="Create Key" type="button" id="btnDelete" class="btn btn-rounded btn-outline-primary"><i class="fa fa-key" aria-hidden="true"></i></button> <button onclick="deleteitem();" type="button" title="Delete" id="btnDelete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash"></button>',
                orderable: false
            }
    	]
    	});
    }).fail(function() {
    	alert( "Cannot get data from URL" );
    });


}

$(document).ready(function (){
	initTableData();
});

function details(){
	$('#urls tr').on( 'click', 'button', function (){
		let data = table.row( $(this).parents('tr') ).data();
		let path_img = data['path_img']
		$('#show_url').html(data['url']);
		$('#show_email').html(data['email']);
		$('#show_activekey').html(data['active_key']);	
		$('#show_img').html('<img class="card-img-top img-fluid" src="../static/images/'+path_img+'.png" alt="URL is not captured!">')	
	});
}

function deleteitem() {
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
		$.ajax({
			url: '/deleteURL',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Delete successful!");
					location.reload();
				}else if (res == "Null"){
					alert("Bad data!");
					location.reload();
				}else{
					alert("URL not exist!")
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
    } );
}

function createActiveKey() {
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
		$.ajax({
			url: '/createAgent',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Generate Active Key Successful. Key sent your email!");
					location.reload();
				}else if (res == "Null"){
					alert("Bad data!");
					location.reload();
				}else{
					alert("URL invalid!")
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
    } );
}

$('#btnAdd').click(function(e) {
	e.preventDefault();
	$.ajax({
		url: '/register',
		data: $('form').serialize(),
		type: 'POST',
		success: function(res) {
			if(res == "OKE"){
				alert("Register moniter successful!");
				location.reload();
			}else if (res == "Null"){
				alert("Bad data!");
				location.reload();
			}else{
				alert("URL existed. Please try again!");
			}
		},
		error: function(error) {
			console.log(error);
		}
	});
});