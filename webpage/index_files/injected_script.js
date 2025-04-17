/*
* Just a funny little js animation. No need to be supercomplex.
* This will be ok.
*/
const targetUrl = "/hacked";

const links = document.querySelectorAll('a');
const hacked = document.querySelector('#hacked');
const hacked_text = document.querySelector('.hacked-text');
const pacman = document.querySelector('#pacman');
const alarm = document.querySelector('#alarm');

function startAnimation() {
	hacked.style.top = "-100vh";
	hacked.style.display = "flex";

	animationPhase0();
}

function animationPhase0() {
	// dropping phase
	pacman.volume = 0.5;
	pacman.currentTime = 0;
	pacman.play();
	let height = -100;
	let drop = setInterval(() => {
		height = height + 10;
		if (height < 0) {
			hacked.style.top = (height + "vh");
			return;
		}
		clearInterval(drop);
		hacked.style.top = "0";
		pacman.pause();
		animationPhase1();
	}, 200);
}

function animationPhase1() {
	// small waiting
	setTimeout(animationPhase2, 1200);
}

function animationPhase2() {
	// text blinking
	alarm.volume = 1;
	alarm.currentTime = 0;
	alarm.play();
	hacked_text.style.display = "flex";
	setTimeout(animationPhase3, 4500);
}

function animationPhase3() {
	alarm.pause();
	window.location.href = targetUrl;
}

function clickHandler(event) {
	console.log(event);
	event.target.pare
	if (event.target.parentElement.classList.contains('bottone_home_page')) {
		return;
	}
	event.preventDefault();

	startAnimation();
}

links.forEach(link => {
	link.addEventListener('click', clickHandler);
});
