
window.addEventListener('message', (event) => {
	if (isNaN(event.data)) {
  	} else {
		sponsorTextWidth = event.data;
		sponsorText = document.querySelectorAll('.resizeSankey');
		sponsorTextWidths = sponsorTextWidth+'px'
		if (sponsorText.length > 0) {
		    if (sponsorText[0]) sponsorText[0].style.width = sponsorTextWidths;
		    if (sponsorText[1]) sponsorText[1].style.width = sponsorTextWidths;
		    if (sponsorText[2]) sponsorText[2].style.width = sponsorTextWidths;
		    if (sponsorText[3]) sponsorText[3].style.width = sponsorTextWidths;
			badge = document.querySelector('.badge');
			if (sponsorTextWidth < 1250) {
				badge.classList.toggle('badge-small', true)
			} else {
				badge.classList.toggle('badge-small', false)
			}
			sponsor = document.querySelector('.sponsor');
			sponcontain = document.querySelector('.spon-contain');
			first = document.querySelector('.first');
			second = document.querySelector('.second');
			third = document.querySelector('.third');
			disclaimer = document.querySelector('.disclaimer');
			sponsortext = document.querySelector('.sponsor-text');
			donatePlz = document.querySelector('.donatePlz');
			if (sponsorTextWidth < 800) {
				sponsor.classList.toggle('sponsor-small', true)
				sponcontain.classList.toggle('spon-contain-small', true)
				first.classList.toggle('first-small', true)
				second.classList.toggle('second-small', true)
				third.classList.toggle('third-small', true)
				disclaimer.classList.toggle('disclaimer-small', true)
				sponsortext.classList.toggle('sponsor-text-small', true)
				donatePlz.classList.toggle('donatePlz-small', true)
			} else {
				sponsor.classList.toggle('sponsor-small', false)
				sponcontain.classList.toggle('spon-contain-small', false)
				first.classList.toggle('first-small', false)
				second.classList.toggle('second-small', false)
				third.classList.toggle('third-small', false)
				disclaimer.classList.toggle('disclaimer-small', false)
				sponsortext.classList.toggle('sponsor-text-small', false)
				donatePlz.classList.toggle('donatePlz-small', false)
			}
		}
	}
})


