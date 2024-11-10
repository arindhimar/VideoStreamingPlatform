(function ($) {
	"use strict";

	var fullHeight = function () {
		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function () {
			$('.js-fullheight').css('height', $(window).height());
		});
	};
	fullHeight();

	$(".toggle-password").click(function () {
		$(this).toggleClass("fa-eye fa-eye-slash");
		var input = $($(this).attr("toggle"));
		input.attr("type", input.attr("type") === "password" ? "text" : "password");
	});
	$.ajax({
		url: '/slideshow/',
		method: 'GET',
		success: function (response) {
			const images = response.images.map(image => image.image_url);
			if (images.length === 0) {
				console.error('No images available for the slideshow.');
				return;
			}

			let currentIndex = Math.floor(Math.random() * images.length);
			$('body').css('background-image', `url(${images[currentIndex]})`);

		},
		error: function (error) {
			console.error('Failed to fetch images:', error);
		}
	});

	$('#submitBtn').on('click', function (e) {
		e.preventDefault(); // Prevent the default form submission

		var username = $('#username').val(); // Get the username from input field
		var password = $('#password').val(); // Get the password from input field
		
		$.ajax({
			url: 'users/login',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				username: username,
				password: password,
			}),
			success: function (response) {
				// Handle successful login response
				alert(response.message);
				// Redirect or perform further actions as needed
			},
			error: function (error) {
				// Handle error response
				alert('Login failed: ' + error.responseJSON.error);
			}
		});
	});

})(jQuery);
