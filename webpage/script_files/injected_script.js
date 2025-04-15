const targetUrl = "/hacked";

const links = document.querySelectorAll('a');

function clickHandler(event) {
	console.log(event);
	event.target.pare
	if (event.target.parentElement.classList.contains('bottone_home_page')) {
		return;
	}
	event.preventDefault();

	const body = document.querySelector("#primo-piano");
	body.style.backgroundColor = "black"; // animation

	setTimeout(() => {
		window.location.href = targetUrl;
	}, 2000);
}

links.forEach(link => {
	link.addEventListener('click', clickHandler);
});
