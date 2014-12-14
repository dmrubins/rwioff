var app = app || {}

app.residentBlockView =  Backbone.View.extend({

	template : _.template( $('#residentBlockTemplate').html() ),

	initialize : function(){
		this.listenTo(this.model, 'change:residents', this.render);
	},

	render: function(){
		residents = this.model.get('residents');
		this.$el.html('');
		residents.each(function(resident){
			t = this.template( resident.toJSON() );
			this.$el.append( t );
		}, this)
		return this;
	}
})