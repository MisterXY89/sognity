

function gen_treemap(selector, uri, c_height, c_width, sentiment) {

  c_height = (c_height == undefined) ? 300 : c_height;
  c_width = (c_width == undefined) ? 300 : c_width;

  // set the dimensions and margins of the graph
  // const margin = {top: 10, right: 10, bottom: 10, left: 10},
  const margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = c_width - margin.left - margin.right,
    height = c_height - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select(selector)
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

  // Read data
  d3.csv(`/read-art-data?uri=${uri}&sentiment=${sentiment}`, function(data) {

    // stratify the data: reformatting for d3.js
    var root = d3.stratify()
      .id(function(d) { return d.name; })   // Name of the entity (column name is name in csv)
      .parentId(function(d) { return d.parent; })   // Name of the parent (column name is parent in csv)
      (data);
    root.sum(function(d) { return +d.value })   // Compute the numeric value for each entity

    // Then d3.treemap computes the position of each element of the hierarchy
    // The coordinates are added to the root object above
    d3.treemap()
      .size([width, height])
      .padding(0)
      (root)

    let mouse_events = get_mouse_events(selector, data, uri);
    const mouseover 	= mouse_events[0];
    const mousemove 	= mouse_events[1];
    const mouseleave	= mouse_events[2];

    // use this information to add rectangles:
    svg
      .selectAll("rect")
      .data(root.leaves())
      .enter()
      .append("rect")
        .attr('x', function (d) { return d.x0; })
        .attr('y', function (d) { return d.y0; })
        .attr('width', function (d) { return d.x1 - d.x0; })
        .attr('height', function (d) { return d.y1 - d.y0; })
        .style("stroke", function(d) { return d.data.color;})
        .style("fill", function(d) { return d.data.color; })
        .on('mouseover', mouseover)
    		.on('mousemove', mousemove)
    		.on('mouseleave', mouseleave);

    // if (uri.includes("track")) {
    //   // add the text labels
    //   svg
    //     .selectAll("text")
    //     .data(root.leaves())
    //     .enter()
    //     .append("text")
    //       .attr("x", function(d){ return d.x0+10})    // +10 to adjust position (more right)
    //       .attr("y", function(d){ return d.y0+20})    // +20 to adjust position (lower)
    //       .text(function(d){ return d.data.name})
    //       .attr("font-size", "15px")
    //       .attr("fill", "white")
    // }
  })
}
