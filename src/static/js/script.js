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

    function removeMessages() {
        $('.flash-message').fadeOut();
    }

    $(document.body).on("click", "p", function(){
        if (this.className.indexOf("word-definition") != -1) {
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
                if (dataObject.data === "true") {
                    object.className = CORRECT_DEFINITION_CLASS;
                    $("#example-container").fadeIn();

                    // TODO: FIll examples
                } else {
                    object.className = WRONG_DEFINITION_CLASS;
                }
            }
        });
    }

    function setWord(data) {
        wordName.html(data[0].name);
        $('.word-definition').remove();
        for (var index in data) {
            wordName.parent().append("<p class='" + DEFINITION_CLASS + "' data-label='"+data[0].label+"'>" + data[index].definition + "</p>");
        }
    }

    window.onload = function () {
        nextWord();
    }
});
