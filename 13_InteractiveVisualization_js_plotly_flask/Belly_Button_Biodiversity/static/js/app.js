function buildMetadata(sample) {

// @TODO: Complete the following function that builds the metadata panel
// Use `d3.json` to fetch the metadata for a sample
// Use d3 to select the panel with id of `#sample-metadata`
// Use `.html("") to clear any existing metadata

// Use `Object.entries` to add each key and value pair to the panel
// Hint: Inside the loop, you will need to use d3 to append new tags for each key-value in the metadata.

// BONUS: Build the Gauge Chart
    
    var url_meta = "/metadata/"+sample
    d3.json(url_meta).then(function(sample_metadata) {
      
    // console.log(Object.entries(sample_metadata)[2][0])

    // add metadata to a container.
    for (i = 0; i < 7; i++) {
      d3.select('#sample-metadata')
      .append('div')
      .text(`${Object.entries(sample_metadata)[i][0]}: ${Object.entries(sample_metadata)[i][1]}`);     
    }
 
//-------------------------------- 
// buildGauge(data.WFREQ);
//-------------------------------- 

var level = Object.entries(sample_metadata)[5][1];

// Trig to calc meter point
var degrees = 180 - level*20,
     radius = .5;
var radians = degrees * Math.PI / 180;
var x = radius * Math.cos(radians);
var y = radius * Math.sin(radians);

// Path: may have to change to create a better triangle
var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
     pathX = String(x),
     space = ' ',
     pathY = String(y),
     pathEnd = ' Z';
var path = mainPath.concat(pathX,space,pathY,pathEnd);

var data = [{ type: 'scatter',
   x: [0], y:[0],
    marker: {size: 28, color:'850000'},
    showlegend: false,
    name: 'speed',
    text: level,
    hoverinfo: 'text+name'},
  { values: [50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50],
  rotation: 90,
  text: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3','1-2', '0-1', ''],
  textinfo: 'text',
  textposition:'inside',
  marker: {colors:['rgb(142, 179, 140)','rgb(147, 186, 145)','rgb(150, 190, 139)','rgb(187, 203, 150)', 'rgb(216, 227, 162)',
                         'rgb(230, 231, 182)', 'rgb(233, 230, 204)', 'rgb(244, 241, 230)', 'rgb(247, 243, 236)',
                         'rgba(255, 255, 255, 0)']},
  labels: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3','1-2', '0-1', ''],
  hoverinfo: 'label',
  hole: .5,
  type: 'pie',
  showlegend: false
}];

var layout = {
  shapes:[{
      type: 'path',
      path: path,
      fillcolor: '850000',
      line: {
        color: '850000'
      }
    }],
  title: 'Belly Button Washing Frequency',
  // height: 1000,
  // width: 1000,
  xaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]},
  yaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]}
};

Plotly.newPlot('gauge', data, layout);

//--------- End of Gauge plot----------------
});
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  // @TODO: Build a Bubble Chart using the sample data
  // @TODO: Build a Pie Chart
  // HINT: You will need to use slice() to grab the top 10 sample_values,
  // otu_ids, and labels (10 each).

    var url = "/samples/"+sample
    
    d3.json(url).then(function(data) {
      
      console.log(data);
      var dataTop = data["sample_values"].slice(0,10);
      console.log(`top 10 ${dataTop}`);
      
      console.log(dataTop);

      var tracePie = {
        labels: data["otu_ids"],
        values: dataTop,
        hovertext: data["otu_labels"],
        type: 'pie'
      };

      var traceBubble = {
        x: data["otu_ids"],
        y: data["sample_values"],
        mode: 'markers',
        hovertext: data["otu_labels"],
        marker: {
          color: data["otu_ids"],
          size: data["sample_values"],
          showscale: true
        }
        
      }
      var layout1 = { margin: { t: 10, b: 200 } };
      var layout2 = { 
        margin: { t: 10, b: 100},
        height: 400,
        xaxes: {title: 'OTU ID'},
    };
      
      Plotly.newPlot("pie", [tracePie], layout1);
      
      Plotly.newPlot("bubble", [traceBubble], layout2);
    });
}

function init() {
  
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options (Create a filter list)
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((col) => {
      selector
        .append("option")
        .text(col)
        .property("value", col);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // clear existing contents of metadata
  document.getElementById("sample-metadata").innerHTML = ""
  
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
