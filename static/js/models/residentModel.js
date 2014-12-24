var app = app || {};

app.residentModel = Backbone.Model.extend({

	defaults : {
		id : null,
		name : null,
		email : null
		preferences : new app.preferencesModel()
	}
	
})