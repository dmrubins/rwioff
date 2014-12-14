var app = app || {};

app.orderWithTitleCollectionView = Backbone.View.extend({

	render: function(){
		this.collection.each(this.addOrder, this);
		return this;
	},

	addOrder: function(order) {
		var orderWithTitleView = new app.orderWithTitleView({ model: order });
		this.$el.append(orderWithTitleView.render().el);
	}

})