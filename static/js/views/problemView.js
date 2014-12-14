var app = app || {};

app.problemView = Backbone.View.extend({

	tagName: "div",
	className: "problem",

	template: _.template( $("#problemTemplate").html() ),

	initialize: function(){
		this.model.get('plan').on('add', this.render, this);
	},

	events : {
		"click" : "select",
		"blur input" : "parsePlan",
		"keypress input" : "parsePlan"
	},

	render: function(){		
		//Add the problem title and thinking to the view
		var problemTemplate = this.template( this.model.toJSON() );
		this.$el.html( problemTemplate );
		
		//Add the orders to the view
		this.model.get('plan').each(this.addPlan, this);
		
		//Add the textbox
		this.$el.append( $('<input type="textbox" id="plan" autofocus />') );

		return this;
	},

	addPlan: function(plan) {
		//console.log(plan);
		var template = _.template( $("#order").html() );
		var planView = new app.planView({ model: plan });

		this.$el.append( planView.render().el );
	},

/***************************************************/
/* EVENTS 
/***************************************************/

	//ON CLICK OF PROBLEM
	select : function() {
		this.$el.find("input").focus();
		app.datamodel.setProblem(this.model);
	},

	//Take manually inputted text and add it to the plan array
	parsePlan: function(e){
		if ( e.type == "keypress" && e.keyCode != 13){ return; }

		//Grab the text of the plan
		var el = $(e.currentTarget)
		var plantext = el.val();
		el.val('');

		//Make sure there is a plan
		if (plantext.trim() == '') { return; }

		//Add the plan to the model
		var plan = new app.planModel({freeForm: plantext})
		this.model.get('plan').add(plan);

		//console.log(this.model.get('plan').toJSON());

		//Re-highlight the textbox
		this.select();
	},

})