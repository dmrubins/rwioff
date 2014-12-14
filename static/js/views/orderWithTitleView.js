var app = app || {};

app.orderWithTitleView = Backbone.View.extend({

	tagName: "tr",

	template: _.template( $("#orderWithTitle").html() ),

	render: function(){
		var t = new app.orderView({ model: this.model });

		var orderTemplate = this.template( this.model.toJSON() );

		this.$el.html( orderTemplate );
		this.$el.find('td.order').append(t.render().el);

		return this;
	}

})