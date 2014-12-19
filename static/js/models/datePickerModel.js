var app = app || {};

app.datePickerModel = Backbone.Model.extend({
	
	defaults : {
		currentDate: new Date()
	},

	setDate : function(date){
		this.set('currentDate', date)
	}
})