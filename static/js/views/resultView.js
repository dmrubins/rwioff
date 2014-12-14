var app = app || {};

app.resultView = Backbone.View.extend({

	tagName: "tr",
	className: "result",

	template: _.template( $("#result").html() ),

	render: function() {
		var resultTemplate = this.template(this.model.toJSON());
		this.$el.html(resultTemplate);
		return this;
	}

})