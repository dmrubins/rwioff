var app = app || {};

app.residentsOffCollection = Backbone.Collection.extend({
	model : app.residentOffForDayModel,

	comparator : function(resident){
		return resident.get('name');
	},

	getEmails : function(){
		var emailStr = '';
		this.each(function(resident){
			name = resident.get('name')
			m = name.match(/(\w*?) (.*)/i);
			emailStr = emailStr + m[2] + ", " + m[1] + ";"
		})
		return emailStr;
	}

})