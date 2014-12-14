var app = app || {}

app.datePickerView = Backbone.View.extend({
	
	template : _.template($('#date').html()),
	dp : $('<div></div>'), 
	heading : $('<div></div>'),

	initialize : function(){
		var s = this;
		this.dp.datepicker({
			onSelect: function(){ 
				s.model.setDate(s.dp.datepicker('getDate')) ;
			} ,
			changeMonth: true,
			changeYear: true,
			yearRange : "2014:2015"
		});

		this.listenTo(this.model, 'change:currentDate', this.updateHeading)

	},

	updateHeading : function (){
		d = {date : $.datepicker.formatDate( "D, M d, yy", this.model.get('currentDate') ) };
		t = this.template( d );
		this.heading.html(t);
	},

	render : function(){
		this.updateHeading();
		this.$el.append(this.heading);
		this.$el.append(this.dp);
		return this;
	}

})