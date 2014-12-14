//Namespace
var app = app || {};

app.resultModel = Backbone.Model.extend({

	defaults: {
		displayName: "null",
		resultValue: "null",
		timeResulted: "now",
		timeCollected: "now"
	},

	initialize: function(){ 
		//console.log("New singleResultModel created.");
	}

});

app.cbcResultModel = app.resultModel.extend({
	defaults : {
		displayName: "CBC",
		resultValue : Array(7.5, 11.0, 33.5, 233)
	}
})