var app = app || {};

app.dataModel = Backbone.Model.extend({
	
	defaults : {
		problem : null,
		order : null
	},

	initialize : function (){
		this.on('change:problem', this.updateProblem, this);
	},

	setProblem : function(problem){
		this.set('problem', problem);
		this.set('order', null);
	},

	setOrder : function(order){
		this.set('order', order)
		this.set('problem', null);
	}


});