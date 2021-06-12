const fetch_Vacci = async () => {


    try{

        const res = await fetch("https://cdn-api.co-vin.in/api/v1/reports/v2/getPublicReports?state_id=&district_id=&date=");
        const data = await res.json();
        console.log(data);

        var vaccinationDetailsAge = data.vaccinationByAge;
        var vaccinationDetails = data.topBlock.vaccination;
        var vacciByState = [...data.getBeneficiariesGroupBy];
        var tableVacci = document.getElementById('vaccineIndia');

        for(var i =0;i<vacciByState.length;++i){

                tableVacci.innerHTML += `<tr style = "scope">
                        <td>${vacciByState[i].title}</td>
                        <td>${vacciByState[i].total}</td>
                        <td>${vacciByState[i].partial_vaccinated}</td>
                        <td>${vacciByState[i].totally_vaccinated}</td>
                </tr>`
        }

        var dataGender = [['Gender','People Vaccinated'],['Male',vaccinationDetails.male],['Female', vaccinationDetails.female],['Others', vaccinationDetails.others]];
        var dataType = [['Type','People Vaccinated'],['Covishield',vaccinationDetails.covishield],['Covaxin', vaccinationDetails.covaxin],['Sputnik', vaccinationDetails.sputnik]];
        var dataAge = [['Age Group','People Vaccinated'],['Age 18 to 45',vaccinationDetailsAge.vac_18_45],['Age 45 to 60', vaccinationDetailsAge.vac_45_60],['Age Above 60',vaccinationDetailsAge.above_60]];
        var OptionGender = {
          title: 'Vaccination Category',
          titleTextStyle:{ color: 'Black' , fontSize: 18 },
          vAxis: {title: 'No. of Vaccination'},
          hAxis: {title: ''},
          seriesType: 'bars',
          series: {1: {type: 'line'}},
          legend: 'none'
        };
        var OptionType = {
          title: 'Vaccination Types',
          titleTextStyle:{ color: 'Black' , fontSize: 18 },
          vAxis: {title: 'No. of Vaccination'},
          hAxis: {title: ''},
          seriesType: 'bars',
          series: {1: {type: 'line'}},
          legend: 'none'
        };

        var OptionAge = {
            title: 'Vaccination by Age',
            titleTextStyle:{ color: 'Black' , fontSize: 18 },
        }

                createChartConfirmed(dataGender, OptionGender, "vacciCategory","comboChart");
                createChartConfirmed(dataType, OptionType, "vacciType","comboChart");
                createChartConfirmed(dataAge, OptionAge, "vacciAge","pieChart");

    }
    catch(err) {
        throw err;
    }

}

fetch_Vacci();