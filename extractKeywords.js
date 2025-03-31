//https://help2.malighting.com/Page/grandMA2/cs_all_keywords/en/3.9

var keywords = document.getElementsByClassName("topic-navigation")[1].getElementsByTagName("ul")[0].getElementsByTagName("li");


var pre = '        {\n          "name": "keyword.other.command.ma2-macro",\n          "match": "\\\\b('
var post = ')\\\\b"\n        },';

var finalStr = "";
var tempList = [];
for(var i = 0; i < keywords.length; i++) {
    var k = keywords[i];
    tempList.push(k.textContent);

    if(tempList.length > 10) {
        finalStr += (pre + tempList.join("|") + post);
        tempList.length = 0;
    }
}
console.log(finalStr);