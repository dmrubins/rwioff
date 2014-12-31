var app = app || {};

app.offTogetherModel = Backbone.Model.extend({
	
	defaults : {
		dates : null,
	},

	initialize : function(){
		this.listenTo(app.dispatcher, "intersect-residents-click", this.intersectResidents)
	},

	intersectResidents : function(residents){
		res_str = '';
		for (var i = 0; i < residents.length; i++){
			res_str = res_str + residents[i].id
		}

		m = this;

		$.ajax('/intersect/' + res_str)
			.done(function(data){
				data = $.parseJSON(data);
				dates = data.dates;		
				dt= Array();
				for (var i = 0; i < dates.length; i++){
					dt.push($.datepicker.parseDate("yymmdd", dates[i]))
				}
				m.set('dates', dt);
				//console.log('setting dates');
			})

	}

})