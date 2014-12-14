var app = app || {};

app.orderView = Backbone.View.extend({

	tagName: "span",

	template: _.template( $("#order").html() ),

	events : {
		'click .order' : "select",
	},

	initialize : function(){
		this.listenTo( this.model, 'change', this.render );
	},

	render: function(){
		var orderTemplate = this.template( this.model.toJSON() );
		this.$el.html( orderTemplate );
		return this;
	}, 

	select : function(){
		app.datamodel.setOrder(this.model);
		return false;
	}

})