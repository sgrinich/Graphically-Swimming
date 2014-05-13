

function onChartButton()
{
    var ajaxURL ='http://thacker.mathcs.carleton.edu/cs257/grinichs/webapp4/createJSON.py';
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open("get", ajaxURL);
    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                onChartButtonCallback(xmlHttpRequest.responseText);

            } 
        }; 

    xmlHttpRequest.send(null);

}

function onChartButtonCallback(text) {
	var times = JSON.parse(text);
    newText = [];

    for (timePair in times[0]) {
        times[0][timePair][1] = Number(times[0][timePair][1]);

    }

    tableDivElement = document.getElementById('testTable');
    
    $.jqplot('chart',times,{
        title:{
            text:'Swim Times VS. Date',
            textColor:'#696969',
            fontSize: '30pt',
        },
        axes:{
            xaxis:{
                tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
                renderer:$.jqplot.DateAxisRenderer,
                label:'Date',
                labelOptions: {
                    textColor:'#696969'
                },
                tickOptions: {
                    fontSize: '10pt',
                    angle: '-30',
                }
            },
            yaxis:{
                tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                label:'Time (seconds)',
                tickOptions: {
                    fontSize: '10pt',

                }
            }},
    });
}
