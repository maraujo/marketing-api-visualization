/**
 * Created by maraujo on 11/21/16.
 */


function getFacebookPopulationInstanceByValue(value){
    for(var instanceIndex in fbInstancesDemographic){
        var instance = fbInstancesDemographic[instanceIndex];
        if(instance[""] == value.toString()){
            return instance;
        }
    }
    return null;
}

function getRectIDFromName(name){
    return name.replace(" ","_")
}

function removeValueFromArray(array,valueToRemove){
    return $.grep(array, function(value) {
        return value != valueToRemove;
    });
}

function buildAndInitVisualComponents(){
    console.log("Building visual components");
    treemapManager = new TreemapManager();
    luxuriousHealthBar = new stackedHorizontalBar();
    GeneralScore = new GeneralScore();
    arabMap = new arabLeagueDatamap();
    sharebleLink = new SharebleLink();
    btnsTopicsSelectors = new BtnsTopicsSelectors();
    historyDataSelector = new HistoryDataSelector();
    findingsFinder = new FindingFinder();
    downloadReport = new DownloadReport();
    console.log("Builded visual components");
    sharebleLink.init();
}

function scoreToPercentage(score){
    return (score * 100).toFixed(1) + "%"
}


function buildBreakPoints(domainBreakpoints, colorRange){
    breakPointsColor = buildBreakPoints(domainLinear, colorRangeScale);
    var breakPoints = [];
    for(var index = 0 in domainBreakpoints){
        var domain = domainBreakpoints[index];
        var color = colorRange[index];
        breakPoints.push({
            "position":domain,
            "color":color
        });
    }
    return breakPoints;
}



function getTooltipLabel(value){
    if(value in mapValuesStringsTooltip){
        return mapValuesStringsTooltip[value];
    } else{
        return value
    }
}

function generateUUID(a){return a?(a^Math.random()*16>>a/4).toString(16):([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,generateUUID)}

function isDemographicCategoryName(name){
    // demographicCategoriesNames = ["age_range","gender","language","exclude_expats","scholarity"]
    demographicCategoriesNames = ["age_range","gender","exclude_expats","scholarity"];
    return demographicCategoriesNames.indexOf(name) >= 0;
}

function convertDataRowsFirstSecondValueToKeyValueDictionary(data){
    var finalDictionary = {};
    for(var subCategoriesIndex = data.rows.length - 1; subCategoriesIndex >= 0; subCategoriesIndex--){
        var rowItem = data.rows[subCategoriesIndex];
        finalDictionary[rowItem[0]] = rowItem[1];
    }
    return finalDictionary;
}

function convertIntegerToReadable(number){
    return numeral(number).format('0.0a');
}

function cloneObject(obj){
    return JSON.parse(JSON.stringify(obj));
}
function removeAllParentheses(string){
    string = string.replace(/\(/g,"");
    string = string.replace(/\)/g,"");
    return string
}

function getJqueryCountryBtnByCode2Letters(countryCode){

    return $("div[data-code='"+ countryCode +"']");
}

function onClickCountryFunctionBy3LettersCode(_3_letters_code){
    var countryCode = convertDatamapsCodeToLocationKey(_3_letters_code);
    var locationItem = getJqueryCountryBtnByCode2Letters(countryCode);
    onClickCountryFunction(locationItem);
}

function onClickCountryFunctionBy2LettersCode(_2_letters_code){
    var locationItem = getJqueryCountryBtnByCode2Letters(_2_letters_code);
    onClickCountryFunction(locationItem);
}

function updateBtnColor(countryCode3Letters, color){
    var _2LetterCountryCode = convertDatamapsCodeToLocationKey(countryCode3Letters);
    var locationItem = getJqueryCountryBtnByCode2Letters(_2LetterCountryCode);
    locationItem.css("background-color",color);
    if(color == DEFAULT_MAP_ARAB_BACKGROUND_COLOR){
        locationItem.css("text-decoration","");
    } else {
        locationItem.css("text-decoration","underline");
    }
}

function onClickCountryFunction(locationItem){
    var countryCode2Letters = locationItem.data("code");
    if(dataManager.isLocationAlreadySelected(countryCode2Letters)){
        dataManager.removeCountryCode(countryCode2Letters);
        locationItem.css("background-color", DEFAULT_MAP_ARAB_BACKGROUND_COLOR);
    } else{
        dataManager.insertCountryCode(countryCode2Letters);
    }
    console.log(dataManager.selectedLocations_2letters);
}

function getCountryNameGivenCode2Letters(countryCode) {
    return locationCodeMap[countryCode].name;
}

function getAllDatamapsCodeInLocationMap(){
    var countryCodes = $.map(locationCodeMap,function (item) {
        return item.datamaps_code;
    });
    return countryCodes;
}

function isDatamapCodeInLocationMap(locationDatamapCode){
    var allDatamapsCodeinLocation = getAllDatamapsCodeInLocationMap();
    for(var locationIndex in allDatamapsCodeinLocation){
        var locationDatamapCodeInList = allDatamapsCodeinLocation[locationIndex];
        if(locationDatamapCodeInList == locationDatamapCode){
            return true;
        }
    }
    return false;
}
function updateFilteringCountryCodeMap(list_country_codes){
    for(var locationKey in locationCodeMap){
        if(list_country_codes.indexOf(locationKey) == -1){
            delete locationCodeMap[locationKey];
            console.log("Deleting")
        }
    }
}

function getLocationsDataGivenKeys(listLocationKeys){
    var listLocationsData = [];
    for(var keyIndex in listLocationKeys){
        var locationKey = listLocationKeys[keyIndex];
        if(locationKey in locationCodeMap){
            listLocationsData.push(locationCodeMap[locationKey]);
        }
    }
    return listLocationsData
}

function sortDictListGivenAttribute(list, attribute) {
    return list.sort(function(a, b) {
        var x = a[attribute]; var y = b[attribute];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}



function updateSocialLinkFields(){
    var fbOriginalURL = "https://www.facebook.com/sharer/sharer.php?u=$LINK&t=Health%20Awareness%20in%20the%20Arab%20World";
    var twitterOriginalUrl = "https://twitter.com/intent/tweet?source=$LINK&text=Health%20Awareness%20in%20the%20Arab%20World:%20$LINK";
    var emailOriginalUrl = "mailto:?subject=Health%20Awareness%20in%20the%20Arab%20World&body=Link:%20$LINK";
    var currentUrl = encodeURIComponent(window.location.href);
    var currentFbHref = fbOriginalURL.replace("$LINK", currentUrl);
    var currentTwitterHref = twitterOriginalUrl.replace("$LINK", currentUrl).replace("$LINK", currentUrl);
    var currentEmailHref = emailOriginalUrl.replace("$LINK", currentUrl);

    $("#facebookShareLink").attr("href",currentFbHref);
    $("#twitterShareLink").attr("href",currentTwitterHref);
    $("#emailShareLink").attr("href",currentEmailHref);

    $("#openGraphImg").attr("content", window.location.origin + window.location.pathname + "imgs/opengraph_sample.png");
    $("#openGraphUrl").attr("content", window.location.href);
}

function convert2LetterCodeToDatamapsCode(_2letters_code){
    for(let key in locationCodeMap) {
        if (locationCodeMap[key]._2letters_code.toUpperCase() == _2letters_code.toUpperCase()) {
            return locationCodeMap[key].datamaps_code;
        }
    }
    Error("2 Letter Code not found:" + _2letters_code);
}

function convertDatamapsCodeToName(datamaps_code){
    try{
        var locationKey = convertDatamapsCodeToLocationKey(datamaps_code);
        return locationCodeMap[locationKey].name;
    }catch (err){
        throw Error("3 Letter Code not found:" + datamaps_code);
    }
}

function convert2LettersCodeToName(_2letters_code){
    for(let key in locationCodeMap) {
        if (locationCodeMap[key]._2letters_code.toUpperCase() == _2letters_code.toUpperCase()) {
            return locationCodeMap[key].name;
        }
    }
    throw Error("2 Letter Code not found:" + _2letters_code);
}

function convertDatamapsCodeToLocationKey(datamaps_code){
    for(var key in locationCodeMap){
        if(locationCodeMap[key].datamaps_code.toUpperCase() == datamaps_code.toUpperCase()){
            return key
        }
    }
    throw Error("3 Letter Code not found:" + datamaps_code);
}

function datenum(v, date1904) {
    if(date1904) v+=1462;
    var epoch = Date.parse(v);
    return (epoch - new Date(Date.UTC(1899, 11, 30))) / (24 * 60 * 60 * 1000);
}

function  initApplicationStaticTexts() {
    $("#applicationTitle").text(APPLICATION_TITLE);
    $("#applicationDescription").text(APPLICATION_DESCRIPTION);
    document.title = APPLICATION_TITLE;
}