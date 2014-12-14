var app = app || {}

app.emailView = Backbone.View.extend({

	events : {
//		"click" : "emailPopup"
	},

	initialize : function(){
		this.listenTo(this.model, 'change:residents', this.adjustEmails)
	},

	adjustEmails : function(){
		emails = this.model.get('residents').getEmails();
		this.$el.prop('href', "mailto:" + emails);
	},

	render : function() {
	}	

})