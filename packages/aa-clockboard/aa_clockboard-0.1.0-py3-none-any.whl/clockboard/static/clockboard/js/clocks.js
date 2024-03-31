function updateClock(clock) {
    let clockElement = document.getElementById("clock" + clock.id);
    let duration = moment.duration(moment() - clock.last_reset, 'milliseconds');
    clockElement.innerHTML = getDurationString(duration);
}

function updateAllClocks() {
    for (let clock of clocks) {
        updateClock(clock);
    }
}