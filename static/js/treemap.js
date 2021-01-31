
// set the dimensions and margins of the graph
var margin = {top: 10, right: 10, bottom: 10, left: 10},
  width = 800 - margin.left - margin.right,
  height = 800 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#song-viz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// spotify:playlist:2QdD7JXzIpyapcfF2QZbUB
const URI = "spotify:playlist:0VOTzMhgX9JA2YHXRl1Vqr";

// Read data
d3.csv('/read-art-data?uri=' + URI, function(data) {

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
    .padding(4)
    (root)

console.log(root.leaves())
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
      .style("fill", function(d) { return d.data.color; });

  // and to add the text labels
  // svg
  //   .selectAll("text")
  //   .data(root.leaves())
  //   .enter()
  //   .append("text")
  //     .attr("x", function(d){ return d.x0+10})    // +10 to adjust position (more right)
  //     .attr("y", function(d){ return d.y0+20})    // +20 to adjust position (lower)
  //     .text(function(d){ return d.data.name})
  //     .attr("font-size", "15px")
  //     .attr("fill", "white")
})
