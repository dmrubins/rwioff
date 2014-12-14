var app = app || {};

app.residentsOffCollection = Backbone.Collection.extend({
	model : app.residentOffForDayModel,

	comparator : function(resident){
		return resident.get('name');
	}

})