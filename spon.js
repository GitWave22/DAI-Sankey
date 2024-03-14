first = document.querySelector('.first');
second = document.querySelector('.second');
third = document.querySelector('.third');


bids = [
  ['small three', 0.25, "url('./Sponsors/bigOne.png') no-repeat center center / contain", "url('./Sponsors/bigTwo.png') no-repeat center center / contain", "url('./Sponsors/smallThree.png') no-repeat center center / contain"],
  ['big one', 3.0, "url('./Sponsors/bigOne.png') no-repeat center center / contain"],
  ['big two', 2.0, "url('./Sponsors/bigOne.png') no-repeat center center / contain", "url('./Sponsors/bigTwo.png') no-repeat center center / contain"],
  ['small one', 1.0, "url('./Sponsors/bigOne.png') no-repeat center center / contain", "url('./Sponsors/bigTwo.png') no-repeat center center / contain", "url('./Sponsors/smallOne.png') no-repeat center center / contain"],
  ['small two', 0.5, "url('./Sponsors/bigOne.png') no-repeat center center / contain", "url('./Sponsors/bigTwo.png') no-repeat center center / contain", "url('./Sponsors/smallTwo.png') no-repeat center center / contain"]
]

bids.sort(function(a, b) {
  return b[1] - a[1];
});


first.style.background = bids[0][2];
second.style.background = bids[1][3];

totalSmallBids = 0.0


for (let i = 2; i < bids.length; i++) { 
  totalSmallBids += bids[i][1];
}



for (let i = 2; i < bids.length; i++) { 
  bidX = (bids[i][1] / totalSmallBids) * 100;
  bidXTwo = bidX.toFixed(1);
  bids[i].push(bidXTwo * 10);
}


probList = []

for (let i = 2; i < bids.length; i++) {
  for (x = 0; x < bids[i][5]; x++) {
    probList.push(bids[i][4]);
  }
}


function randomIntFromInterval(min, max) { // min and max included 
  return Math.floor(Math.random() * (max - min + 1) + min)
}

probListOut = {}

function thirdPicker() {
  third.style.background = probList[randomIntFromInterval(0, probList.length - 1)];
}

thirdPicker()
setInterval(thirdPicker, 5000); 