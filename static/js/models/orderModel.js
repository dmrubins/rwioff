var app = app || {};

app.orderModel = Backbone.Model.extend({

	defaults: {
		category: GENERAL_CARE,
		displayName: "Null",  
		order: "undefined",
		results: new app.resultCollection(),
		isConfirmed : true
	},

	initialize: function(){
		//console.log( this.toJSON() );
	}

});