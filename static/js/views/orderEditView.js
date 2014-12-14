var app = app || {};

app.orderEditView = Backbone.View.extend({
	tag: "div",
	template: _.template( $("#orderEditView").html() ), 

	events : {
		'blur' : 'update',
		'keypress' : 'update'
	},

	render : function() {
		this.$el.html( this.template( this.model.toJSON() ) );
		return this;
	},

	update : function(e){
		alert(e.type);
		if ( e.type == "keypress" && e.keyCode != 13){ return; }
		this.model.set('displayName', this.$el.find('input').val() );
	},

	select : function(){
		this.$el.find('input').select();
	}
	
})