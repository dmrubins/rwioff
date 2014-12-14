var app = app || {};

app.orderWithTitleCollectionView = Backbone.View.extend({

	render: function(){
		this.collection.each(this.addOrder, this);
		return this;
	},

	addOrder: function(order) {
		var singleOrderView = new app.orderView({ model: order });
		this.$el.append(orderView.render().el);
	}

})