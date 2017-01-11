/**
 * Created by maki on 1/11/2017.
 */
WordView = function (wordModelList) {
    this._wordModelList = wordModelList;
    this._i = 0;

    this.getNextModel = function () {
        if (this._i >= this._wordModelList.length) return false;

        var ret_value = this._wordModelList[this._i];
        this._i++;
        return ret_value;
    };
    this.isLast = function () {
        return this._i == this._wordModelList.length;
    };
    this.getCurrentWord = function () {
        return this._wordModelList[this._i - 1].word;
    };
    this.getI = function(){
        return this._i;
    };
};

$(document).ready(function () {
    $('.button-collapse').sideNav();
    $('.modal').modal();
    window.setTimeout(function () {
        $('.flash-message').fadeOut();
    }, 2000);
});

$(document).ready(function () {

    var domainUrl = "http://127.0.0.1:5000";

    var DEFINITION_CLASS = "word-definition card-panel";
    var WRONG_DEFINITION_CLASS = "word-definition card-panel wrong-definition";
    var CORRECT_DEFINITION_CLASS = "word-definition card-panel correct-definition";
    var TWITTER_PARAGRAPH_CLASS = "word-example card-panel teal";
    var WIKIPEDIA_PARAGRAPH_CLASS = "word-example card-panel teal";
    var DONE_CLASS = "stop-answering";

    var wordNumberContainer = $("#word-number");
    var skipNext = $("#skip-next");
    var wordView;
    var pressed_incorrect = false, pressed_correct = false;
    var last = false;

    fillViewModel();
    function fillViewModel() {
        var urlNextWord = domainUrl + "/next_word";
        $.post(urlNextWord, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            var data = dataObject.data;
            if (dataObject.success) {
                wordView = new WordView(data);
            }
            setNextWord();
        });
    }

    function setNextWord() {
        var data = wordView.getNextModel();
        if (data !== false) {
            wordNumberContainer.html(wordView.getI().toString()+"/10");
            $("#word-name").html(data.word.name);
            var container = $('#word-definition-container');
            $('.word-definition').remove();
            for (var index in data.definitions) {
                container.append("<p class='" + DEFINITION_CLASS + "' data-label='" + data.word.label + "'>"
                    + data.definitions[index] + "</p>");
            }
        } else {
            // TODO: ako dodje do kraja
        }
    }

    $(document.body).on("click", "p", function () {
        if (this.className.indexOf("word-definition") == -1) return;
        if (pressed_correct) return;
        var object = this;

        var word = wordView.getCurrentWord();
        var word_url = word.name + "/" + object.innerHTML + "/" + word.label;
        var urlCheckWord = domainUrl + "/check_word/" + word_url;
        $.post(urlCheckWord, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.success && dataObject.data) { // if the answer is correct
                object.className = CORRECT_DEFINITION_CLASS;
                pressed_correct = true;
            } else {
                object.className = WRONG_DEFINITION_CLASS;
                pressed_incorrect = true;
            }
            if (pressed_correct) {
                getTwitterExamples(word);
                $("#example-container").fadeIn();
                getWikipediaExamples(word);

                if (wordView.isLast()) {
                    skipNext.html("FINISH");
                    skipNext.addClass("finished");
                }
                var correct = 1;
                if (pressed_incorrect) correct = 0;
                var urlSeen = domainUrl + "/seen-word/" + word_url + "/" + correct;
                $.post(urlSeen, function (jsonData) {
                    console.log(jsonData)
                });
            }
        });
    });

    skipNext.click(function () {
        if (this.className.indexOf("finished") !== -1)
        {
            var urlFinished = domainUrl +"/finished";
            document.location = urlFinished;
        }

        $('.word-definition').each(function (i) {
            $(this).fadeOut('slow');
        });
        $('.word-example').each(function (i) {
            $(this).fadeOut('slow');
        });
        $('#example-container').fadeOut();
        pressed_incorrect = false
        pressed_correct = false;
        setNextWord();
    });

    function getTwitterExamples(word) {
        var urlTwitterExamples = domainUrl + "/twitter-example/" + word.name + "/" + word.definition + "/" + word.label;
        $.post(urlTwitterExamples, function (jsonData) {
            try {
                var dataObject = JSON.parse(jsonData);
                if (dataObject.success) {
                    console.log(dataObject);
                    var twitterContainer = $('#twitter');
                    for (var i in dataObject.data.statuses) {
                        twitterContainer.append("<p class='" + TWITTER_PARAGRAPH_CLASS + "'>" + dataObject.data.statuses[i] + "</p>");
                    }
                }
            }
            catch (err) {
                console.log(err);
            }
        })
    }
    function getWikipediaExamples(word) {
        var urlWikipediaExamples = domainUrl + "/wikipedia-example/" + word.name + "/" + word.definition + "/" + word.label;
        $.post(urlWikipediaExamples, function (jsonData) {
            var dataObject = JSON.parse(jsonData);
            if (dataObject.success && dataObject.data != []) {
                console.log(dataObject);
                var wikipediaContainer = $('#wikipedia');
                for (var i in dataObject.data) {
                    wikipediaContainer.append("<p class='" + WIKIPEDIA_PARAGRAPH_CLASS + "'>" + dataObject.data[i] + "</p>");
                }
            }
        })
    }
});
