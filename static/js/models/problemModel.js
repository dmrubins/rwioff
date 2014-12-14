var app = app || {};

app.problemModel = Backbone.Model.extend({

	ORM : new app.orderRecognitionModel(),

	defaults: {
		title: "Undefined",
		medicalDecisionMaking: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci magna, laoreet eu arcu in, consectetur sollicitudin ligula. Fusce eleifend.",
		plan: new app.planCollection([]),
	},


/***************************************************/
/* METHODS
/***************************************************/
	getResults : function(){
		return this.getOrderResults(LAB_ORDER);
	},

	getConsults : function(){
		return this.getOrderResults(CONSULT_ORDER);
	}, 

	getOrderResults : function(orderCategory){
		var results = new app.resultCollection();
		this.get('plan').each(function(p){
			//Get the orders
			orders = p.get('associatedOrders');
			if (orders == null) return null;

			//Cycle through the orders for lab orders
			orders.each(function(o){
				if (o.get('category') == orderCategory){
					o.get('results').each(function(r){
						results.add(r);
					}, this); 
				}
			}, this);
		}, this);
		return results;
	}
















});