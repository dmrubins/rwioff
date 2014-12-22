var app = app || {};

app.residentsCollection = Backbone.Collection.extend({
	model : app.residentModel,

	comparator : function(resident){
		return resident.get('name');
	},

	getEmails : function(){
		var emailStr = '';
		this.each(function(resident){
			name = resident.get('name')
			m = name.match(/(\w*?) (.*)/i);
			try{
				emailStr = emailStr + m[2] + ", " + m[1] + ";"
			}catch(Error)
			{}
		})
		return emailStr;
	}

})