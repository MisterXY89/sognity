
function show_results(res_list) {
	let search_results = $("#search-results");
	let html = "";
	res_list.forEach((track, index) => {
		search_results.append(`<div class='col-2'>
				<div class="">
				  <img class="card-img-top" src="${track.album_image}" alt="album cover">
				  <div class="card-body bg-dark text-light">
				    <a href="${track.href}" target="blank_"><h5 class="card-title">${track.track_name}</h5></a>
				    <p class="card-text">by ${track.artists}, ${track.album_name}</p>
				    <a href="#select-${index}" id="result-no-${index}" class="btn btn-outline-light select-search-result">Select</a>
				  </div>
				</div>
			</div>`);
		});
		$(".carousel").css("transform", "translateY(0%)");
		// console.log(html);
		// search_results.html(html);
}


document.addEventListener("DOMContentLoaded", evt => {

	let state = 0;

	// $('.carousel').carousel();
	$('.carousel').carousel('pause');

	const start = $("#start");
	const small_logo = $("#small-logo");
	const search_field = $("#search-field");
	const switch_view_btn = $("#switch-view");
	const search_btn = $("#search-btn");
	const select_search_result_btns = $(".select-search-result");

	switch_view_btn.click( evt => {
		state = 0;

		$('.carousel').carousel("next");
		small_logo.fadeIn();
		$("#songName").focus();

	});


	search_btn.click( evt => {
		state = 1;

		let query = $("#songName").val();
		let url = "/search?q=" + query;
		if (query.length <= 2) {
			alert("Please enter at least *3* characters to search for.");
			return 0;
		} else {

			console.log(url);
			fetch(url)
			.then(resp => resp.json())
			.then(json => {
				console.log(json);
				let res_list = [];
				json.forEach(track => {
					res_list.push({
						track_name: track.name,
						track_id: track.uri.split(":").slice(-1)[0],
						album_name: track.album.name,
						album_image: track.album.images[1].url,
						href: track.href,
						artists: track.artists.map(a => a.name).join(",")
					});
				});
				console.log(res_list);
				show_results(res_list);
				$('.carousel').carousel("next");
			});

		}
	});

	// select_search_result_btns.on('click', evt => {
	$(document).on('click', '.select-search-result', function () {
		let source = $(this).attr("id");
		console.log(source);
	});


	$(document).keypress(function(e) {
		if(e.which == 13) {
			switch (state) {
				case 0:
					switch_view.click();
					break;
				case 1:
					search_btn.click();
					break;
				default:
					console.log("ENTER switch default.");
					break;
			}
		}
	});

});
