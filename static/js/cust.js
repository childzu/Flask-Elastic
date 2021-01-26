$(function(){
	$('#search_txt').keyup(function(){
		var keyword = $('#search_txt').val();
		$.ajax({
			url: '/api/search',
			data: {'q': keyword},
			type: 'GET',
			success: function(response){
                $('#no_of_cust').html('Found : ' + response.length);
                var content = $("#content_data");
                content.html('');
                $.each(response, function (index, data) {
                    var html = 
                    '<article class="post">' +
                        '<header>' +
                            '<div>' +
                                '<h1>' + data.firstName + ' ' + data.lastName + '</h1>' +
                                '<div class="about">Age ' + data.age + '</div>' +
                            '</div>' +
                        '</header>' +
                        '<p class="body">' + data.email + '</p>' +
                    '</article>' +
                    '<hr>';
                    content.append(html);
                });
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});