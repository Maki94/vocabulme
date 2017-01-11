$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.modal').modal();
});

$(document).ready(function () {
    var domainUrl = "http://127.0.0.1:5000";
    var wordName = $('#word-name');

    var DEFINITION_CLASS = "word-definition card-panel";
    var WRONG_DEFINITION_CLASS = "word-definition card-panel wrong-definition";
    var CORRECT_DEFINITION_CLASS = "word-definition card-panel correct-definition";
    var TWITTER_PARAGRAPH_CLASS = "word-example card-panel teal";
    var WIKIPEDIA_PARAGRAPH_CLASS = "word-example card-panel teal";
    var DONE_CLASS = "stop-answering";
    
    function removeMessages() {
        $('.flash-message').fadeOut();
    }

    $(document.body).on("click", "p", function(){
        var correctParagraph = $("."+DONE_CLASS);
        if (this.className.indexOf("word-definition") != -1 && correctParagraph.length === 0) {
            if (this.className == WRONG_DEFINITION_CLASS || this.className == CORRECT_DEFINITION_CLASS) return;
            console.log(this.innerHTML);
            console.log(document.getElementById("word-name").innerHTML);
            console.log(this.dataset.label);
            var data = {name:document.getElementById("word-name").innerHTML, definition:this.innerHTML, label:this.dataset.label};
            checkWord(data, this);
        }
    });

    window.setTimeout(removeMessages, 2000);

    $("#skip-next").click(function () {
        $('.word-definition').each(function (i, obj) {
            $(this).fadeOut('slow');
        });
        $('.word-example').each(function (i, obj) {
            $(this).fadeOut('slow');
        });
        $("#example-container").fadeOut();
        nextWord();
    });

    function nextWord() {
        var urlNextWord = domainUrl + "/next_word";
        $.post(urlNextWord, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.success) {
                setWord(dataObject.data);
            }
        });
    }

    function checkWord(word, object) {
        var urlCheckWord = domainUrl + "/check_word/" + word.name + "/" + word.definition + "/" + word.label;
        $.post(urlCheckWord, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.success) {
                if (dataObject.data) {
                    object.className = CORRECT_DEFINITION_CLASS+" "+DONE_CLASS;
                    seenWord(word, 1);
                    $("#example-container").fadeIn();
                    getTwitterExamples(word);
                    setTimeout(getWikipediaExamples(word), 100);
                } else {
                    object.className = WRONG_DEFINITION_CLASS;
                    seenWord(word, 0);
                }
            }
        });
    }
    function setWord(data) {
        wordName.html(data[0].name);
        var container = $('#word-definition-container');
        $('.word-definition').remove();
        for (var index in data) {
            container.append("<p class='" + DEFINITION_CLASS + "' data-label='"+data[0].label+"'>" + data[index].definition + "</p>");
        }
    }

    function getTwitterExamples(word){
        var urlTwitterExamples = domainUrl + "/twitter-example/" + word.name + "/" + word.definition + "/" + word.label;
        $.post(urlTwitterExamples, function (jsonData) {
            try{
                var dataObject = JSON.parse(jsonData);
                if (dataObject.success) {
                    console.log(dataObject);
                    var twitterContainer = $('#twitter');
                    for (var i in dataObject.data.statuses){
                        twitterContainer.append("<p class='"+TWITTER_PARAGRAPH_CLASS+"'>"+dataObject.data.statuses[i]+"</p>");
                    }
                }
            }
            catch(err){
                console.log(err);
            }
        })
    }
    function seenWord(word, correct){
        var urlWikipediaExamples = domainUrl + "/seen-word/" + word.name + "/" + word.definition + "/" + word.label + "/" + correct;
        $.post(urlWikipediaExamples, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.data){
                console.log("seen_word");
            }
        });
    }
    function getWikipediaExamples(word){
        var urlWikipediaExamples = domainUrl + "/wikipedia-example/" + word.name + "/" + word.definition + "/" + word.label;
        $.post(urlWikipediaExamples, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.success && dataObject.data != []) {
                console.log(dataObject);
                var wikipediaContainer = $('#wikipedia');
                for (var i in dataObject.data){
                    wikipediaContainer.append("<p class='"+WIKIPEDIA_PARAGRAPH_CLASS+"'>"+dataObject.data[i]+"</p>");
                }
            }
        })
    }
    nextWord();
});
