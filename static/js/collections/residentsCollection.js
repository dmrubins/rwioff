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
	},

	getAllResidents : function() {
		r = this;
		$.ajax('/residents/')
			.done(function(data){
				data = $.parseJSON(data);
				names = data.names;
				ids = data.ids;
				emails = data.emails;
				for (var i = 0; i < names.length; i++){
					r.add(new app.residentModel({'name': names[i], 'id' : ids[i]}) ) ;//, 'email' : emails[i]}) ) ;
				}
				app.dispatcher.trigger('set:residents');
			})	
	},

	getNamesAndIds : function() {
		namesAndIds = Array();
		this.each(function(resident){
			namesAndIds.push({'name' : resident.get('name'), 'id' : resident.get('id')})
		});
		return namesAndIds;
	},

})