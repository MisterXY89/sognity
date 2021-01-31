
function get_mouse_events(selector, data, uri) {

	if (uri.includes("playlist")) {
		return null;
	}

	// TOOL-TIP & MOUSE EVENTS
	const Tooltip = d3.select(selector)
		.append("div")
		.style("opacity", 0)
		.attr("class", "tooltip")
		.style("background-color", "white")
		.style("border", "solid")
		.style("border-width", "2px")
		.style("border-radius", "0px")
		.style("padding", "5px");

	// Three function that change the tooltip when user hover / move / leave a cell
	var mouseover = () => {
		Tooltip
			.style("opacity", 1);
	}
	var mousemove = (d) => {
		console.log(d);
		Tooltip
			.html(
				`${'<table style="width:100%">'
						+ '<tr>'
								+ '<th>Section</th>'
								+ '<td>'}${d.data.name}</td>`
					  + '</tr>'
						+ '<tr>'
								+ '<th>Value</th>'
								+ `<td>${d.data.value}</td>`
						+ '</tr>'
						+ '<tr>'
								+ '<th>Loudness</th>'
								+ `<td>${d.data.loudness}</td>`
						+ '</tr>'
						+ '<tr>'
								+ '<th>Key</th>'
								+ `<td>${d.data.key}</td>`
						+ '</tr>'
						+ '<tr>'
								+ '<th>Tempo</th>'
								+ `<td>${d.data.tempo}</td>`
						+ '</tr>'
				+ '</table>',
			)
			// .style("left", `${d3.event.pageX+90-width}px`)
			// .style("top", `${d3.event.pageY-height/2+70}px`)
			// .style("left", `${d3.event.pageX+0}px`)
			// .style("top", `${d3.event.pageY-50}x`)
			.style('border-color', d.data.color);
	}
	var mouseleave = () => {
		Tooltip.style("opacity", 0)
	}

	return [
		mouseover,
		mousemove,
		mouseleave
	]
}
