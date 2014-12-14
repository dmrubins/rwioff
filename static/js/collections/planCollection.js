var app = app || {};

app.planCollection = Backbone.Collection.extend({

	model: new app.planModel(),

	initialize : function(){
		this.on('add', this.parse );
	},

	addOrders : function(c){
		c.each(this.addOrder, this);
	},

	addOrder : function(o){
		var p = new app.planModel({ freeForm: "#order", associatedOrders: new app.orderCollection([o]) });
		this.add(p);
		//console.log(this); 
	},

	parse : function() {
		this.each(function(p){
			var plantext = p.freeForm;
			app.ORM.parse( p );
		}, this);
	}

})