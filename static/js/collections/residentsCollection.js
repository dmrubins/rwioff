var app = app || {};

app.residentsCollection = Backbone.Collection.extend({
	model : app.residentModel,

	comparator : function(resident){
		return resident.get('name');
	},

	getEmails : function(){
		var emailStr = '';
		this.each(function(resident){
			email = resident.get('email')
			try{
				emailStr = emailStr + email + ";"
			}catch(Error)
			{}
		})
		return emailStr;
	}

})