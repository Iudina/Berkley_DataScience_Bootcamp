// from data.js
var tableData = data;

function fulltable() {
// create a table, add data to a table
    var tbody = d3.select("tbody");
    tableData.forEach(function(sighting) {
    var row = tbody.append("tr");
    Object.entries(sighting).forEach(function([key, value]) {;
        // Append a cell to the row for each value in data report object
        var cell = tbody.append("td");
        cell.text(value);
    });
    });
};

fulltable()

var submit = d3.select("#filter-btn");

submit.on("click", function() {
    
    // clear existing table
    document.getElementById("to-be-filtered").innerHTML = "";
    
    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Select the input element and get the raw HTML node
    var inputDate = d3.select("#datetime");
     // Get the value property of the input element
    var inputDateValue = inputDate.property("value");

    var inputCity = d3.select("#city");
    var inputCityValue = inputCity.property("value");

    var inputState = d3.select("#state");
    var inputStateValue = inputState.property("value");

    var inputCountry = d3.select("#country");
    var inputCountryValue = inputCountry.property("value");

    var inputShape = d3.select("#shape");
    var inputShapeValue = inputShape.property("value");

    // // display full table if filter is empty
    // if (inputValue == "") {fulltable()};

    var filteredData = tableData.filter(function(sighting) {
        return (sighting.datetime === inputDateValue || inputDateValue === "") &&
            (sighting.city === inputCityValue || inputCityValue === "") &&
            (sighting.state === inputStateValue || inputStateValue === "") &&
            (sighting.country === inputCountryValue || inputCountryValue === "") &&
            (sighting.shape === inputShapeValue || inputShapeValue === "");
    });
        

    // var func = function(sighting) { return sighting.datetime === inputDateValue; };
    // var filteredData = tableData.filter(func);

    // Arrow function
    // var filteredData = tableData.filter(sighting => sighting.datetime === inputDateValue);
    

  console.log(filteredData);

  var tbody = d3.select("tbody");
  filteredData.forEach(function(sighting) {
    var row = tbody.append("tr");
    Object.entries(sighting).forEach(function([key, value]) {;
      // Append a cell to the row for each value in data report object
      var cell = tbody.append("td");
      cell.text(value);
    });
  });

});
