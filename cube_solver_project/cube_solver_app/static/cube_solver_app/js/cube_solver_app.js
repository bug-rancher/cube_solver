
var colors = new Array(6);

var stickerMatrix = createStickerMatrix();

var activeColor;


document.addEventListener("DOMContentLoaded", function () { afterLoad(); }, false);
$("#button").click( function (event) { sendRequest() } );

function createStickerMatrix() 
{
    let matrix = new Array(9);
    
    for (let i=0; i<3; i++) 
    {
        matrix[i] = new Array(3);
    }
    
    for (let i=3; i<6; i++) 
    {
        matrix[i] = new Array(12);
    }
    
    for (let i=6; i<9; i++) 
    {
        matrix[i] = new Array(3);
    }
    
    return matrix;
}

function afterLoad() 
{
    setCentresColors();
    setBarColors();
    setBarColorsEvents();
    setStickerEvents();
}

function setCentresColors()
{
    $("#1_1").css("background-color", "white");
    $("#4_1").css("background-color", "green");
    $("#4_4").css("background-color", "red");
    $("#4_7").css("background-color", "blue");
    $("#4_10").css("background-color", "orange");
    $("#7_1").css("background-color", "yellow");
}

function setBarColors() 
{
    $("#c_0").css("background-color", "white");
    $("#c_1").css("background-color", "green");
    $("#c_2").css("background-color", "red");
    $("#c_3").css("background-color", "blue");
    $("#c_4").css("background-color", "orange");
    $("#c_5").css("background-color", "yellow");
}

function setBarColorsEvents() 
{
    for (let i=0; i<6; i++) 
    {
        colors[i] = document.getElementById("c_" + i);
        colors[i].addEventListener("click", function () { getColor("c_" + i) });
    }
}

function getColor(id) 
{
    activeColor = $("#" + id).css("background-color");
}

function setStickerEvents() 
{
    for (let i=0; i<9; i++) 
    {
        for (let j=0; j<12; j++) 
        {
            if ((i<3 || i>5) && (j>2)) 
            {
                continue;
            }
            else 
            {
                stickerMatrix[i][j] = document.getElementById(i + "_" + j);
                stickerMatrix[i][j].addEventListener("click", function () { setColor(i + "_" + j) });
            }
        }
    }
}

function setColor(id) 
{
    $("#" + id).css("background-color", activeColor);
}

function sendRequest() 
{
    let layoutInJSON = createLayoutInJSON();
    
    $.get('/solve/', {layout: layoutInJSON}, function (response) { displayResults(response) } );
}

function createLayoutInJSON() 
{
    let layout = getColorsFromLayout();
    
    return JSON.stringify(layout);
}

function getColorsFromLayout() 
{
    let layout = new Array(0);
    
    for (let i=0; i<9; i++) 
    {
        let row = new Array(0);
        
        for (let j=0; j<12; j++) 
        {
            if ((i<3 || i>5) && (j>2)) 
            {
                continue;
            }
            else 
            {
                let stickerColor = $("#" + i + "_" + j).css("background-color");
                
                row.push(stickerColor);
            }
        }
        
        layout.push(row);
    }
    
    return layout;
}

function displayResults(response)
{
    let parsedResponse = JSON.parse(response);
    
    let isError = parsedResponse.is_error;
    
    if (isError)
    {
        displayCaution();
    }
    else 
    {
        displayNotation();
    }
    
    displayMoves(parsedResponse, isError);
}

function displayCaution() 
{
    let CautionHTML;
    
    CautionHTML = createHeaderCaution();
    
    CautionHTML += 
        '<p>Correct marked stickers on layout and click "solve" again</p>';
    
    $("#description").html(CautionHTML); 
}

function displayNotation() 
{
    let symbols = ['F', 'R', 'B', 'L', 'U', 'D'];
    let words = ['front', 'right', 'back', 'left', 'up', 'down'];
    
    let notationHTML;
    
    notationHTML = createHeaderNotation();
    
    notationHTML += '<table>';
            
    for (let i=0; i<6; i++) 
    {
        notationHTML += 
            '<tr>' +
                '<td><b>' + symbols[i] + '</b></td>' + 
                '<td>turn ' + words[i] + ' face 90&deg; clockwise</td>' +
            '</tr>' +
            '<tr>' +
                '<td><b>' + symbols[i] + '\'</b></td>' + 
                '<td>turn ' + words[i] + ' face 90&deg; counterclockwise</td>' +
            '</tr>' +
            '<tr>' +
                '<td><b>' + symbols[i] + '2</b></td>' + 
                '<td>turn ' + words[i] + ' face 180&deg;</td>' +
            '</tr>';
    }
    
    notationHTML += '</table>';
    
    $("#description").html(notationHTML); 
}

function displayMoves(parsedResponse, isError) 
{
    let movesHTML;
    
    if (isError)
    {
        movesHTML = createHeaderError();
    }
    else 
    {
        movesHTML = createHeaderMoves();
    }
    
    let amount = Object.keys(parsedResponse.moves).length;
    
    movesHTML += createMoves(parsedResponse, amount);
    
    $("#moves").html(movesHTML);
    
    for (let i=0; i<amount; i++) 
    {
        colorizeLayouts(parsedResponse.moves[i].layout, i);
    }
}

function createMoves(parsedResponse, amount) 
{
    let movesHTML;
    
    movesHTML = 
        '<table>' +
            '<col width="40">' + 
            '<col width="90">' + 
            '<col width="320">';
    
    for (let i=0; i<amount; i++) 
    {
        let number = parsedResponse.moves[i].number;
        let symbol = parsedResponse.moves[i].move_symbol;
        let layoutTable = createLayoutTable(parsedResponse.moves[i].layout, i);
   
        let oneMoveHTML = 
            "<tr>" +
                '<td class="number">' + number + "</td>" +
                '<td class="symbol">' + symbol + "</td>" +
                "<td>" + layoutTable + "</td>" +
            "</tr>";

        movesHTML += oneMoveHTML;
    }
    
    movesHTML += "</table>";
    
    return movesHTML;
}

function createLayoutTable(parsedLayout, nr) 
{
    let layoutTalbe;
    
    layoutTable =
        '<table>' +
            '<tr>'+
               '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_0_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_0_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_0_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_1_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_1_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_1_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_2_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_2_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_2_2"></div>' +
                '</td>' +
            '</tr>' +
            '<tr>'+
                '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_3_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_4_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_5_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_2"></div>' +
                '</td>' +
                '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_3_3"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_4"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_5"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_4_3"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_4"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_5"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_5_3"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_4"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_5"></div>' +
                '</td>' +
                '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_3_6"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_7"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_8"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_4_6"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_7"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_8"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_5_6"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_7"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_8"></div>' +
                '</td>' +
                '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_3_9"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_10"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_3_11"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_4_9"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_10"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_4_11"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_5_9"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_10"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_5_11"></div>' +
                '</td>' +
            '</tr>' +
            '<tr>'+
               '<td class="faceSolution">' +             
                    '<div class="stickerSolution" id="' + nr + '_6_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_6_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_6_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_7_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_7_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_7_2"></div>' +
                
                    '<div class="stickerSolution" id="' + nr + '_8_0"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_8_1"></div>' +
                    '<div class="stickerSolution" id="' + nr + '_8_2"></div>' +
                '</td>' +
            '</tr>' +
        '</table>';

    return layoutTable;
}

function colorizeLayouts(parsedLayout, nr) 
{
    for (let i=0; i<9; i++) 
    {
        for (let j=0; j<12; j++) 
        {
            if ((i<3 || i>5) && (j>2)) 
            {
                continue;
            }
            else 
            {
                if (parsedLayout[i][j] == "rgb(0, 0, 0)")
                {
                    let bgColor = $("#" + nr + "_" + i + "_" + j).addClass("stickerSolutionBad");
                    bgColor.removeClass("stickerSolution");
                }
                else 
                {
                    let bgColor = $("#" + nr + "_" + i + "_" + j).css("background-color", parsedLayout[i][j]);
                }
            }
        }
    }
}

function createHeaderError() 
{
    let headerHTML = 
        '<div class="sticky" id="headerLeft">' +
            '<div id="numberHeader">' + 'nr' + '</div>' +
            '<div id="symbolHeader">' + 'error' + '</div>' +
            '<div id="layoutHeader">' + 'layout' + '</div>' +
        '</div>';
    
    return headerHTML;
}

function createHeaderMoves() 
{
    let headerHTML = 
        '<div class="sticky" id="headerLeft">' +
            '<div id="numberHeader">' + 'nr' + '</div>' +
            '<div id="symbolHeader">' + 'symbol' + '</div>' +
            '<div id="layoutHeader">' + 'layout' + '</div>' +
        '</div>';
    
    return headerHTML;
}

function createHeaderCaution() 
{
    let headerHTML = 
        '<div class="sticky" id="headerRight">' +
            '<div id="caution">' + 'caution' + '</div>' +
        '</div>';
    
    return headerHTML;
}

function createHeaderNotation() 
{
    let headerHTML = 
        '<div class="sticky" id="headerRight">' +
            '<div id="caution">' + 'notation' + '</div>' +
        '</div>';
    
    return headerHTML;
}
