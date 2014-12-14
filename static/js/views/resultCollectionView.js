var app = app || {};

app.resultCollectionView = Backbone.View.extend({

	tagName: "div",

	render: function(){
		this.collection.each(this.addResult, this);
		return this;
	},

	addResult: function(result) {
		//console.log(result.toJSON());
		var singleView = new app.resultView({ model: result });
		this.$el.append(singleView.render().el);
	}

})