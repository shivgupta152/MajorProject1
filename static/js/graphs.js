 function createChartConfirmed(dataParam,options,elementContainer,chartType){
 google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawVisualization);

      function drawVisualization() {
        // Some raw data (not necessarily accurate)
        var data = google.visualization.arrayToDataTable(dataParam);

//        var options = {
//          title : 'Monthly Coffee Production by Country',
//          vAxis: {title: 'Cups'},
//          hAxis: {title: 'Month'},
//          seriesType: 'bars',
//          series: {1: {type: 'line'}}
//        };

        if(chartType === 'comboChart')
            var chart = new google.visualization.ComboChart(document.getElementById(elementContainer));

        if(chartType === 'pieChart')
            var chart = new google.visualization.PieChart(document.getElementById(elementContainer));


        chart.draw(data, options);
      }
 }