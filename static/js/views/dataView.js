var app = app || {};

app.dataView = Backbone.View.extend({
	
	blanktemplate: _.template( $("#data").html() ),
	problemtemplate: _.template( $("#problemView").html() ),
	ordertemplate: _.template( $('#orderEditView').html() ),
	view: null,
	problem: null,
	order: null,

	initialize : function(){
		this.template = this.blanktemplate;
		this.model.on("change:problem", this.update, this);
		this.model.on("change:order", this.update, this);
	},

	render: function(){
		return this;
	},

/***************************************************/
/* EVENTS 
/***************************************************/
	update : function() {
		
		//Problem selected
		this.problem = this.model.get('problem');
		if (this.problem != null){
			this.template = this.problemtemplate;

			this.view = {
				//ordersView : this.updateOrdersView(),
		 		resultsView : this.updateResultsView(),
				//this.updateImagingView();
		 		consultsView : this.updateConsultsView()
			}
			this.$el.html( this.problemtemplate(this.view) );
		}
		
		this.order = this.model.get('order');
		if (this.order != null) {
			var oev = new app.orderEditView({ model : this.order });
			this.$el.html( oev.render().el );
			oev.select();
		}

		this.render();
	},

/***************************************************/
/* PROBLEM SPECIFIC VIEWS
/***************************************************/
	
	updateOrdersView : function() {
		var oc = this.problem.getOrders();
	},

	updateResultsView : function() {
		var resultsCollection = this.problem.getResults();
		var rcv = new app.resultCollectionView({ collection: resultsCollection });
		return rcv.render().$el.html();
	},

	updateImagingView : function (){

	},

	updateConsultsView : function(){
		var consultsCollection = this.problem.getConsults();
		var ccv = new app.resultCollectionView({ collection : consultsCollection });
		return ccv.render().$el.html();
	}

})
