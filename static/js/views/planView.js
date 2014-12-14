var app = app || {};

app.planView = Backbone.View.extend({

	tagName: "div",
	orderViews: Array(),
	template: _.template( $('#plan').html() ),

	render: function(){
		var freeForm = this.model.get('freeForm');
		var re = /#order/gi;
		
		//Put spans in for all the orders
		freeForm = freeForm.replace(re, "<span class='prelim'></span>");

		//prelim render
		this.$el.html(this.template({ freeForm: freeForm }));

		//Get the spans
		var spans = this.$el.find('.prelim');

		//Get the view for the orders
		var orders = this.model.get('associatedOrders');
		if (orders != null)	{

			//Make each order view
			orders.each(this.renderOrderViews, this);
		
			//Place the orders in the plan
			for (var i=0; i < this.orderViews.length; i++){
				$(spans[i]).append(this.orderViews[i]);
			}
		}

		return this;		
	},

	renderOrderViews : function(o) {
		var orderView = new app.orderView({ model : o });
		this.orderViews.unshift( orderView.render().$el );
	}

})