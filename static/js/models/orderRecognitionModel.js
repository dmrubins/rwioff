var app = app || {};

app.orderRecognitionModel = Backbone.Model.extend({


	parse : function(p){
		re = /Type and Screen/i;
		ff = p.get('freeForm');
		var n = ff.search(re);
		if ( n < 0 ) return;
		p.set('freeForm', ff.replace(re, "#order"));
		order = new app.orderModel({category: LAB, displayName: 'Type and Screen', isConfirmed: false});
		p.addOrder(order);
	}


})
app.ORM = new app.orderRecognitionModel();