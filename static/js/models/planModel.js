var app = app || {};

app.planModel = Backbone.Model.extend({
	
	defaults: {
		freeForm: "Null",
		associatedOrders : new app.orderCollection()
	},

	addOrder : function(o) {
		this.get('associatedOrders').add(o);
	}
})