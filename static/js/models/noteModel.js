var app = app || {};

app.noteModel = Backbone.Model.extend({

	defaults{
		problems: new app.problemCollection({});
	}

})