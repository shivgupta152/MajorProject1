const fetch_cases = async () => {
    try {
        const res = await fetch("https://api.covid19india.org/data.json");
        const data = await res.json();
        console.log(data);
        var table = document.getElementById("casesIndia");
        var statewise = [...data.statewise];
        var allTimeData = [...data.cases_time_series];
        var activeIndia = document.getElementById("activeCasesIndia");
        activeIndia.innerHTML=statewise[0].active;
        var confirmedIndia = document.getElementById("confirmedCasesIndia");
        confirmedIndia.innerHTML = statewise[0].confirmed;
        var deathsIndia = document.getElementById("deathsIndia");
        deathsIndia.innerHTML = statewise[0].deaths;
        var recoveredIndia = document.getElementById("recoveredIndia");
        recoveredIndia.innerHTML = statewise[0].recovered;

//        var table = document.getElementById("casesIndia");



        var dataDates = [];
        var dataConfirmed = [['Date','Confirmed Cases','Trend']];
//        var dataActive =[];
        var dataRecovered =[['Date','Recovered Patients','Trend']];
        var dataDeceased =[['Date','Deceased Patients','Trend']];
        var counter = 0;

        for(var i = 0; i < allTimeData.length; i+= 7) {
//            dataDates.push(allTimeData.date);
            dataConfirmed.push([allTimeData[i].date, parseInt(allTimeData[i].dailyconfirmed), parseInt(allTimeData[i].dailyconfirmed)]);
            dataRecovered.push([allTimeData[i].date, parseInt(allTimeData[i].dailyrecovered), parseInt(allTimeData[i].dailyrecovered)]);
            dataDeceased.push([allTimeData[i].date, parseInt(allTimeData[i].dailydeceased), parseInt(allTimeData[i].dailydeceased)]);

//
//            dataDeceased.push(allTimeData.dailydeceased);
        }

        var optionsConfirmed = {
          title : 'Cases Confirmed Weekly',
          titleTextStyle:{ color: 'Black' , fontSize: 16 },
          vAxis: {title: 'No. of Cases Confirmed'},
          hAxis: {title: '', textColor: '#ffffff'},
          seriesType: 'bars',
          series: {1: {type: 'line'}},
          legend: 'none'
        };
        var optionsRecovered = {
          title : 'Patients Recovered Weekly',
          titleTextStyle:{ color: 'Black' , fontSize: 16 },
          vAxis: {title: 'No. of Patients Recovered' },
          hAxis: {title: '', textColor: '#ffffff'},
          seriesType: 'bars',
          series: {1: {type: 'line'}},
          legend: 'none'
        };
         var optionsDeceased = {
          title : 'Patients Deceased Weekly',
          titleTextStyle:{ color: 'Black' , fontSize: 16 },
          vAxis: {title: 'No. of Patients Deceased'},
          hAxis: {title: '', textColor: '#ffffff'},
          seriesType: 'bars',
          series: {1: {type: 'line'}},
          legend: 'none'
        };

        createChartConfirmed(dataConfirmed, optionsConfirmed, "chartConfirmed","comboChart");
        createChartConfirmed(dataRecovered, optionsRecovered, "chartRecovered","comboChart");
        createChartConfirmed(dataDeceased, optionsDeceased, "chartDeceased","comboChart");



              simplemaps_countrymap.hooks.ready = function (){
                for(var i = 1;i<statewise.length;++i){
                            if(statewise[i].state === "State Unassigned") {
                                continue;
                            }
                            table.innerHTML += `<tr scope="row">
                                        <td>${statewise[i].state}</td>
                                        <td>${statewise[i].confirmed}</td>
                                        <td>${statewise[i].active}</td>
                                        <td>${statewise[i].deaths}</td>
                                        <td>${statewise[i].recovered}</td>
                                    </tr>`;
                //                    console.log(simplemaps_countrymap_mapdata.state_specific[i].description)
                            simplemaps_countrymap.mapdata.state_specific[i].description = statewise[i].confirmed;

                        }
                        console.log(simplemaps_countrymap_mapdata)
                        simplemaps_countrymap.load();
            }
            simplemaps_countrymap.hooks.ready();
//                    console.log(simplemaps_countrymap_mapdata.state_specific)
                    console.log(simplemaps_countrymap)
//                    createChartConfirmed(data, options, elementContainer)

    } catch(err) {
        throw err;
    }
}

fetch_cases();
